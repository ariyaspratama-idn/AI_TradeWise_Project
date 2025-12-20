# src/modules/market_analysis/indicator_engine.py
import pandas as pd
import numpy as np

class IndicatorEngine:
    def __init__(self, df):
        self.df = df.copy()

    def ema(self, span=10):
        self.df[f"EMA_{span}"] = self.df["close"].ewm(span=span, adjust=False).mean()
        return self.df

    def macd(self):
        ema12 = self.df["close"].ewm(span=12, adjust=False).mean()
        ema26 = self.df["close"].ewm(span=26, adjust=False).mean()
        self.df["MACD"] = ema12 - ema26
        self.df["Signal_Line"] = self.df["MACD"].ewm(span=9, adjust=False).mean()
        return self.df

    def bollinger_bands(self, window=20):
        self.df["SMA"] = self.df["close"].rolling(window=window).mean()
        self.df["Upper_BB"] = self.df["SMA"] + (self.df["close"].rolling(window=window).std() * 2)
        self.df["Lower_BB"] = self.df["SMA"] - (self.df["close"].rolling(window=window).std() * 2)
        return self.df

    def rsi(self, period=14):
        delta = self.df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / (loss + 1e-10)
        self.df["RSI"] = 100 - (100 / (1 + rs))
        return self.df

    def all_indicators(self):
        self.ema(10)
        self.macd()
        self.bollinger_bands()
        self.rsi()
        return self.df.fillna(0)
