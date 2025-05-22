import requests
from cachetools import cached, TTLCache
from config import COINMARKETCAP_API_KEY, COINMARKETCAP_API_URL, REQUEST_TIMEOUT
import json

cache = TTLCache(maxsize=100, ttl=300)


@cached(cache)
def get_market_data(coin_id: str) -> dict:
    """Get market data from CoinMarketCap"""
    try:
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY
        }

        params = {
            'symbol': coin_id.upper(),
            'convert': 'USD'
        }

        response = requests.get(
            f"{COINMARKETCAP_API_URL}/cryptocurrency/quotes/latest",
            headers=headers,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        # Добавляем детальное логирование
        print(f"CoinMarketCap API response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:200]}...")  # Логируем первые 200 символов

        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"API error response: {error_data}")
            except:
                print("API returned non-JSON error response")
            return {}

        data = response.json()

        # Проверка структуры ответа
        if 'data' not in data or coin_id.upper() not in data['data']:
            print(f"Unexpected API response structure: {data}")
            return {}

        coin_data = data['data'][coin_id.upper()]
        quote = coin_data['quote']['USD']

        return {
            'market_cap': quote.get('market_cap', 0),
            'rank': coin_data.get('cmc_rank', 0),
            'price_change_24h': quote.get('percent_change_24h', 0),
            'volume_24h': quote.get('volume_24h', 0)
        }

    except requests.exceptions.RequestException as e:
        print(f"Market data request failed: {str(e)}")
        return {}
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return {}
    except Exception as e:
        print(f"Unexpected error fetching market data: {str(e)}")
        return {}