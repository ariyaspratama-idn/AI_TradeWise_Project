import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from modules.market_data.data_fetcher import MarketDataFetcher

def test_market_data():
    print("Testing MarketDataFetcher...")
    fetcher = MarketDataFetcher()
    
    # Test Binance (usually works without key)
    print("Fetching Binance data...")
    res = fetcher.fetch_binance(symbol="BTCUSDT", limit=5)
    if res["status"]:
        print("Binance Fetch Success!")
        print(res["data"].head())
    else:
        print(f"Binance Fetch Failed: {res.get('msg')}")

if __name__ == "__main__":
    test_market_data()
