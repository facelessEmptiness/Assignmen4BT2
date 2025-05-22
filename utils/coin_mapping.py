# Mapping between coin names and API-specific identifiers
COIN_MAPPING = {
    'bitcoin': {
        'ticker': 'BTC',
        'coinmarketcap_id': 'BTC',  # Символ для CoinMarketCap
        'cryptopanic_id': 'BTC'
    },
    'ethereum': {
        'ticker': 'ETH',
        'coinmarketcap_id': 'ETH',
        'cryptopanic_id': 'ETH'
    },
    # ... add all top 50 coins
}

def get_coin_metadata(coin_name: str) -> dict:
    """Get all API identifiers for a coin"""
    return COIN_MAPPING.get(coin_name.lower(), {})