import requests
from cachetools import cached, TTLCache
from config import CRYPTO_PANIC_API_KEY, REQUEST_TIMEOUT

cache = TTLCache(maxsize=100, ttl=300)  # 5 minute cache

@cached(cache)
def get_crypto_news(coin_name: str, limit: int = 3) -> list:
    """Fetch latest news for a cryptocurrency"""
    try:
        params = {
            'auth_token': CRYPTO_PANIC_API_KEY,
            'filter': 'rising',
            'currencies': coin_name.upper()
        }
        response = requests.get(
            'https://cryptopanic.com/api/v1/posts/',
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()['results'][:limit]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []