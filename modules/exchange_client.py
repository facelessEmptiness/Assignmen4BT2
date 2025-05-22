import requests
from cachetools import cached, TTLCache
from config import BINANCE_API_URL, REQUEST_TIMEOUT

cache = TTLCache(maxsize=100, ttl=60)  # 1 minute cache for prices

@cached(cache)
def get_current_price(ticker: str) -> float:
    """Get current price from Binance"""
    try:
        symbol = f"{ticker.upper()}USDT"
        response = requests.get(
            f"{BINANCE_API_URL}/ticker/price",
            params={'symbol': symbol},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return float(response.json()['price'])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return 0.0