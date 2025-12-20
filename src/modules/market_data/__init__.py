# src/modules/market_data/__init__.py
"""
Modul pengelolaan data pasar:
- Pengambilan data dari berbagai sumber (saham, forex, kripto, komoditas)
- Pembersihan dan normalisasi data
- Penyimpanan cache agar cepat diakses oleh modul analisis & AI
"""

from .data_fetcher import MarketDataFetcher
from .data_preprocessor import MarketDataPreprocessor
from .cache_manager import CacheManager
from .data_sources import DataSourceManager
