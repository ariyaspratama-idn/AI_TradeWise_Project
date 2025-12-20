# src/modules/market_data/data_preprocessor.py
import pandas as pd
import numpy as np

class MarketDataPreprocessor:
    def __init__(self):
        pass

    def normalize(self, df, columns=None):
        if columns is None:
            columns = ["open", "high", "low", "close", "volume"]
        df_norm = df.copy()
        for col in columns:
            min_val = df[col].min()
            max_val = df[col].max()
            df_norm[col] = (df[col] - min_val) / (max_val - min_val)
        return df_norm

    def add_indicators(self, df):
        df["SMA_5"] = df["close"].rolling(window=5).mean()
        df["SMA_20"] = df["close"].rolling(window=20).mean()
        df["RSI"] = self._calculate_rsi(df["close"])
        df["EMA_10"] = df["close"].ewm(span=10, adjust=False).mean()
        df["MACD"] = df["EMA_10"] - df["close"].ewm(span=26, adjust=False).mean()
        return df.fillna(0)

    def _calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        return rsi
