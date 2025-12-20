# =========================================================
#  AI TradeWise Project - Backend Entry Point
#  Author: Ariyas Pratama
#  Description:
#     Backend utama sistem AI Trading & Investment Assistant
#     Menyediakan REST API, login JSON, AI konsultasi, analisis pasar,
#     dan sistem notifikasi multikanal (WA/Telegram/Email).
# =========================================================

from flask import Flask, request, jsonify
import os
import json
import threading
import sys
from datetime import datetime
from dotenv import load_dotenv

# VERCEL PATH FIX: Ensure 'src' directory is in Python path
# This allows 'from modules import ...' to work even if Vercel runs from root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import modul internal
from modules.notifications import NotificationManager
from modules.data_validation import DataValidator
from modules.market_analysis import MarketAnalyzer
from modules.market_data import MarketDataFetcher
from modules.ai_consultation import AIConsultationManager
from modules.multi_model import MultiAIModel
from utils.logger import Logger
from utils.config import Config

# =========================================================
# INITIALIZATION
# =========================================================
# Fix: Point static folder to ../frontend and url_path to /
import os
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
app = Flask(__name__, static_folder=template_dir, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

load_dotenv()

logger = Logger("main_logger")
config = Config()
data_validator = DataValidator()
market_analyzer = MarketAnalyzer()
market_data = MarketDataFetcher()
ai_manager = AIConsultationManager(platform="web")
multi_model = MultiAIModel()
notify = NotificationManager()

# ... (Previous code)

# =========================================================
# DETECT VERCEL ENVIRONMENT
# =========================================================
# Vercel filesystem is Read-Only. We must use /tmp for temp storage.
IS_VERCEL = os.getenv("VERCEL") == "1"

if IS_VERCEL:
    DATA_DIR = "/tmp"
else:
    # Local development
    DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.json")

# =========================================================
# 1. AUTO-CREATE ADMIN DEFAULT
# =========================================================
def initialize_admin():
    try:
        users = []
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                try:
                    users = json.load(f)
                except:
                    users = []
        
        # Check if admin exists
        if not any(u.get("username") == "admin" for u in users):
            users.append({
                "username": "admin",
                "password": "admin123",
                "role": "admin",
                "created_at": datetime.now().isoformat()
            })
            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=4)
            logger.log("Admin default initialized.")
            
    except Exception as e:
        logger.log(f"Init Admin Error: {str(e)}")

# Wrap initialization in try-except to prevent startup crash on Vercel
try:
    if not IS_VERCEL:
        initialize_admin()
    else:
        # On Vercel, we might skip file writing or handle it gracefully
        # Try to initialize but pass if fails
        try:
           initialize_admin()
        except:
           pass
except Exception:
    pass

# =========================================================
# 2. USER AUTHENTICATION
# =========================================================
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    users = load_users()

    if any(u["username"] == username for u in users):
        return jsonify({"status": "error", "message": "Username sudah terdaftar"}), 400

    users.append({
        "username": username,
        "password": password,
        "role": "user",
        "created_at": datetime.now().isoformat()
    })
    save_users(users)
    logger.log(f"User baru terdaftar: {username}")
    return jsonify({"status": "success", "message": "Registrasi berhasil!"})

@app.route("/login", methods=["POST"])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return jsonify({
                "status": "success",
                "message": "Login berhasil!",
                "user": {"username": username, "role": user["role"]}
            })
    return jsonify({"status": "error", "message": "Username atau password salah"}), 401



# =========================================================
# 3. AI CONSULTATION
# =========================================================
@app.route("/consult", methods=["POST"])
def consult_ai():
    data = request.json
    user_id = data.get("user_id", "guest")
    question = data.get("question", "")

    preferred_model = data.get("preferred_model")

    # Ambil data pasar real-time
    context = {
        "signal_data": market_analyzer.get_latest_signal(),
        "sentiment": market_analyzer.get_sentiment(),
        "preferred_model": preferred_model
    }

    response = ai_manager.handle_user_query(user_id, question, context)
    logger.log(f"[AI Chat] {user_id}: {question} -> {response['response']}")
    return jsonify(response)

# =========================================================
# 4. MARKET DATA & ANALYSIS
# =========================================================
@app.route("/market-data", methods=["GET"])
def get_market_data():
    data = market_data.fetch_latest()
    return jsonify(data)

@app.route("/market-analysis", methods=["GET"])
def analyze_market():
    report = market_analyzer.generate_full_report()
    return jsonify(report)

# =========================================================
# 5. NOTIFICATIONS
# =========================================================
@app.route("/notify", methods=["POST"])
def send_notification():
    data = request.json
    channel = data.get("channel", "telegram")
    message = data.get("message", "Notifikasi dari AI TradeWise")

    success = notify.send(channel=channel, message=message)
    return jsonify({"status": "sent" if success else "failed"})

# =========================================================
# 6. PERIODIC UPDATER (REALTIME MARKET WATCHER)
# =========================================================



def load_alerts():
    if not os.path.exists(ALERTS_FILE):
        return []
    try:
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_alerts(alerts):
    os.makedirs(os.path.dirname(ALERTS_FILE), exist_ok=True)
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

@app.route("/add-alert", methods=["POST"])
def add_alert():
    data = request.json
    alerts = load_alerts()
    
    new_alert = {
        "id": len(alerts) + 1,
        "asset": data.get("asset"),
        "condition": data.get("condition"),
        "target_value": float(data.get("value", 0)),
        "channel": data.get("channel"),
        "contact": data.get("contact"), # Save custom contact
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    alerts.append(new_alert)
    save_alerts(alerts)
    logger.log(f"Alert baru ditambahkan: {new_alert}")
    return jsonify({"status": "success", "message": "Alert berhasil dibuat!"})

# =========================================================
# 6. PERIODIC UPDATER (REALTIME MARKET WATCHER)
# =========================================================
def check_alerts(market_data_snapshot):
    # Skip alert checking if we are on Vercel unless manually triggered
    # In full production, this should be a separate Cron Job service.
    if IS_VERCEL:
        return 

    alerts = load_alerts()
    active_alerts = [a for a in alerts if a["status"] == "active"]
    
    # Simple mapping for demo assets
    # In real app, map symbols correctly
    current_prices = {}
    if "details" in market_data_snapshot:
        for item in market_data_snapshot["details"]:
            try:
                # Remove comma if any and convert to float
                price_str = str(item["price"]).replace(",", "")
                current_prices[item["symbol"]] = float(price_str)
            except:
                continue

    for alert in active_alerts:
        asset = alert["asset"]
        if asset in current_prices:
            current_price = current_prices[asset]
            target = alert["target_value"]
            condition = alert["condition"]
            contact = alert.get("contact") # Retrieve stored contact
            
            triggered = False
            if condition == "price_above" and current_price > target:
                triggered = True
            elif condition == "price_below" and current_price < target:
                triggered = True
            
            if triggered:
                msg = f"🔔 ALERT: {asset} telah mencapai {current_price} ({condition} {target})!"
                # Pass contact as 'to' parameter
                notify.send(alert["channel"], msg, to=contact)
                alert["status"] = "triggered" # trigger once
                save_alerts(alerts)
                logger.log(f"Alert triggered: {msg}")

def background_market_updater():
    import time
    while True:
        try:
            data = market_analyzer.generate_full_report() # Use analyzer to get simulated data
            check_alerts(data)
            logger.log("Market check complete.")
        except Exception as e:
            logger.log(f"Updater error: {str(e)}")
        time.sleep(60)  # Check every 60 seconds

if not IS_VERCEL:
    # Disable background loop on Vercel to prevent Lambda timeout/freeze issues.
    # On Vercel, usage is event-driven only.
    threading.Thread(target=background_market_updater, daemon=True).start()
else:
    logger.log("Background updater disabled for Vercel Environment.")

# =========================================================
# 7. CONFIG ENDPOINT (FOR FRONTEND)
# =========================================================
@app.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "twilio_sandbox_code": os.getenv("TWILIO_SANDBOX_CODE", "join unknown-code")
    })

# =========================================================
# 8. START SERVER
# =========================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
 