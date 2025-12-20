# src/modules/market_data/cache_manager.py
import os
import pandas as pd

class CacheManager:
    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, name):
        return os.path.join(self.cache_dir, f"{name}.csv")

    def save_to_cache(self, name, df):
        path = self._get_cache_path(name)
        df.to_csv(path, index=False)

    def load_from_cache(self, name):
        path = self._get_cache_path(name)
        if os.path.exists(path):
            return pd.read_csv(path)
        return None

    def list_cache(self):
        return [f for f in os.listdir(self.cache_dir) if f.endswith(".csv")]

    def clear_cache(self):
        for f in self.list_cache():
            os.remove(os.path.join(self.cache_dir, f))
        return {"status": True, "msg": "Cache cleared."}