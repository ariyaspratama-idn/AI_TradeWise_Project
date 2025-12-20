# src/modules/market_analysis/ai_signal_generator.py
import numpy as np

class AISignalGenerator:
    def __init__(self, df=None, sentiment="neutral"):
        self.df = df
        self.sentiment = sentiment

    def generate_signal(self, df=None):
        if df is not None:
            self.df = df
        
        if self.df is None:
            return {"signal": "HOLD", "confidence": "Neutral"}

        last = self.df.iloc[-1]
        ema_signal = "BUY" if last["close"] > last["EMA_10"] else "SELL"
        macd_signal = "BUY" if last["MACD"] > last["Signal_Line"] else "SELL"
        rsi_signal = "BUY" if last["RSI"] < 30 else ("SELL" if last["RSI"] > 70 else "HOLD")

        combined = [ema_signal, macd_signal, rsi_signal]
        score = combined.count("BUY") - combined.count("SELL")

        if self.sentiment == "bullish":
            score += 1
        elif self.sentiment == "bearish":
            score -= 1

        if score > 1:
            return {"signal": "BUY", "confidence": "High"}
        elif score == 1:
            return {"signal": "BUY", "confidence": "Moderate"}
        elif score == 0:
            return {"signal": "HOLD", "confidence": "Neutral"}
        elif score == -1:
            return {"signal": "SELL", "confidence": "Moderate"}
        else:
            return {"signal": "SELL", "confidence": "High"}
