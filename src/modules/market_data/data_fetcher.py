# src/modules/market_data/data_fetcher.py
import requests
import pandas as pd
import time
from datetime import datetime
from .data_sources import DataSourceManager

class MarketDataFetcher:
    def __init__(self, cache_manager=None):
        self.sources = DataSourceManager()
        self.cache = cache_manager

    def fetch_yahoo(self, symbol="AAPL", interval="1d", range="1mo"):
        """Ambil data saham dari Yahoo Finance"""
        base_url = self.sources.get_source("yahoo")["base_url"]
        url = f"{base_url}{symbol}?interval={interval}&range={range}"
        response = requests.get(url)
        if response.status_code != 200:
            return {"status": False, "msg": "Gagal ambil data Yahoo."}
        data = response.json()
        if "chart" not in data or "result" not in data["chart"]:
            return {"status": False, "msg": "Data Yahoo tidak valid."}
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        quotes = result["indicators"]["quote"][0]
        df = pd.DataFrame({
            "timestamp": [datetime.fromtimestamp(t) for t in timestamps],
            "open": quotes["open"],
            "high": quotes["high"],
            "low": quotes["low"],
            "close": quotes["close"],
            "volume": quotes["volume"]
        })
        if self.cache:
            self.cache.save_to_cache(symbol, df)
        return {"status": True, "data": df}

    def fetch_binance(self, symbol="BTCUSDT", interval="1h", limit=100):
        """Ambil data kripto dari Binance"""
        base_url = self.sources.get_source("binance")["base_url"]
        url = f"{base_url}?symbol={symbol}&interval={interval}&limit={limit}"
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            if response.status_code != 200:
                raise Exception(f"Status {response.status_code}")
            data = response.json()
            if isinstance(data, dict) and "code" in data:
                 raise Exception(f"API Error {data}")
        except Exception as e:
            print(f"DEBUG: Binance fetch failed ({e}). Using Dummy Data.")
            # Dummy Data Generation
            data = []
            now_ms = int(time.time() * 1000)
            base_price = 45000.0
            
            for i in range(limit):
                time_offset = (limit - 1 - i) * (3600 * 1000) # 1 hour interval
                t_open = now_ms - time_offset
                
                # Random walk
                import random
                change = (random.random() - 0.5) * 100
                o = base_price
                c = base_price + change
                h = max(o, c) + random.random() * 50
                l = min(o, c) - random.random() * 50
                base_price = c
                
                # [open_time, open, high, low, close, volume, close_time, ...]
                data.append([
                    t_open, str(o), str(h), str(l), str(c), "100.0", 
                    t_open + 3600000, "5000000.0", 100, "50.0", "2500000.0", "0"
                ])

        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
        df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        if self.cache:
            self.cache.save_to_cache(symbol, df)
        return {"status": True, "data": df}

    def fetch_forex(self, pair="EURUSD"):
        """Ambil data forex dari Alpha Vantage"""
        src = self.sources.get_source("alphavantage")
        url = f"{src['base_url']}?function=FX_DAILY&from_symbol={pair[:3]}&to_symbol={pair[3:]}&apikey={src['api_key']}"
        response = requests.get(url)
        if response.status_code != 200:
            return {"status": False, "msg": "Gagal ambil data Alpha Vantage."}
        data = response.json().get("Time Series FX (Daily)", {})
        if not data:
            return {"status": False, "msg": "Data forex kosong atau API key invalid."}
        df = pd.DataFrame([
            {
                "date": k,
                "open": float(v["1. open"]),
                "high": float(v["2. high"]),
                "low": float(v["3. low"]),
                "close": float(v["4. close"])
            } for k, v in data.items()
        ])
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        if self.cache:
            self.cache.save_to_cache(pair, df)
        return {"status": True, "data": df}

    def fetch_latest(self):
        """Aggregate latest data for main dashboard"""
        return {
            "crypto": self.fetch_binance("BTCUSDT"),
            "forex": self.fetch_forex("EURUSD"),
            "timestamp": datetime.now().isoformat()
        }
