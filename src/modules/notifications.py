import os
import requests
import smtplib
from email.mime.text import MIMEText

class NotificationManager:
    def __init__(self):
        pass

    def send(self, channel, message, to=None):
        """
        Mengirim notifikasi ke channel yang dipilih.
        Parameter 'to' opsional untuk override tujuan default .env
        """
        try:
            if channel == "telegram":
                return self._send_telegram(message, to)
            elif channel == "email":
                return self._send_email(message, to)
            elif channel == "whatsapp":
                return self._send_whatsapp(message, to)
            else:
                print(f"[LOG NOTIF] {channel} -> {to}: {message}")
                return True
        except Exception as e:
            print(f"[NOTIF ERROR] Gagal mengirim ke {channel}: {e}")
            return False

    def _send_whatsapp(self, message, to=None):
        """Kirim WA via Twilio API"""
        sid = os.getenv("TWILIO_ACCOUNT_SID")
        token = os.getenv("TWILIO_AUTH_TOKEN")
        from_wa = os.getenv("TWILIO_FROM_NUMBER")
        to_wa = to if to else os.getenv("TWILIO_TO_NUMBER") # Use custom or default

        if not sid or not token or not from_wa or not to_wa:
            print("[WhatsApp] Konfigurasi Twilio belum lengkap")
            return False

        try:
            from twilio.rest import Client
            client = Client(sid, token)
            
            # Ensure whatsapp: prefix
            if not to_wa.startswith("whatsapp:"):
                to_wa = f"whatsapp:{to_wa}"
                
            msg = client.messages.create(
                body=message,
                from_=from_wa,
                to=to_wa
            )
            return True if msg.sid else False
        except Exception as e:
            print(f"[WhatsApp API Error] {e}")
            return False

    def _send_telegram(self, message, to=None):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = to if to else os.getenv("TELEGRAM_CHAT_ID")
        
        if not token or not chat_id:
            return False
            
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try:
            res = requests.post(url, json=payload, timeout=10)
            return res.status_code == 200
        except:
            return False

    def _send_email(self, message, to=None):
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        receiver = to if to else os.getenv("EMAIL_RECEIVER")
        
        if not sender or not password or not receiver:
             return False
             
        msg = MIMEText(message)
        msg['Subject'] = "AI TradeWise Alert"
        msg['From'] = sender
        msg['To'] = receiver
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"[Email Error] {str(e)}")
            return False
