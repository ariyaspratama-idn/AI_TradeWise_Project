# src/modules/market_data/data_sources.py
import os
from dotenv import load_dotenv

load_dotenv()

class DataSourceManager:
    def __init__(self):
        self.sources = {
            "yahoo": {
                "type": "stock",
                "base_url": "https://query1.finance.yahoo.com/v8/finance/chart/"
            },
            "binance": {
                "type": "crypto",
                "base_url": "https://api.binance.com/api/v3/klines"
            },
            "alphavantage": {
                "type": "forex",
                "base_url": "https://www.alphavantage.co/query",
                "api_key": os.getenv("ALPHAVANTAGE_API_KEY")
            }
        }

    def get_source(self, name):
        return self.sources.get(name)

    def list_sources(self):
        return list(self.sources.keys())
