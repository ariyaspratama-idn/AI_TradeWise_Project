from .ai_signal_generator import AISignalGenerator
from .sentiment_analyzer import SentimentAnalyzer
from .report_generator import ReportGenerator

class MarketAnalyzer:
    def __init__(self):
        self.signal_gen = AISignalGenerator()
        self.sentiment = SentimentAnalyzer()
        self.report_gen = ReportGenerator()

    def get_latest_signal(self):
        # Stub or delegate
        return self.signal_gen.generate_signal() # Example default

    def get_sentiment(self):
        return "Neutral" # Stub

    def generate_full_report(self):
        # Simulasi data pasar yang lebih kaya untuk demo
        import random
        from datetime import datetime
        
        assets = [
            {"symbol": "BTC/USD", "type": "Crypto", "price": 95000 + random.randint(-500, 500)},
            {"symbol": "ETH/USD", "type": "Crypto", "price": 3500 + random.randint(-50, 50)},
            {"symbol": "EUR/USD", "type": "Forex", "price": 1.05 + random.uniform(-0.01, 0.01)},
            {"symbol": "XAU/USD", "type": "Commodity", "price": 2650 + random.randint(-10, 10)},
        ]
        
        details = []
        for asset in assets:
            # Generate random signal based on simulation
            signal_res = self.signal_gen.generate_signal() # Returns {signal, confidence}
            details.append({
                "symbol": asset["symbol"],
                "type": asset["type"],
                "price": f"{asset['price']:.2f}",
                "signal": signal_res.get("signal", "HOLD"),
                "confidence": signal_res.get("confidence", "Neutral"),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "overall_sentiment": "Bullish" if random.random() > 0.5 else "Bearish",
            "details": details
        }
