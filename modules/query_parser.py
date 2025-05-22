def parse_user_query(query: str) -> dict:
    """Extract cryptocurrency and query type from user input"""
    # Basic implementation - can be enhanced with NLP
    query = query.lower()

    # Map of common cryptocurrency names to their standard tickers
    coin_mapping = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'solana': 'SOL',
        # ... add other top 50 coins
    }

    # Identify coin
    coin = next((c for c in coin_mapping if c in query), None)

    # Identify query type
    query_types = {
        'news': any(word in query for word in ['news', 'update', 'headline']),
        'price': any(word in query for word in ['price', 'cost', 'value']),
        'market': any(word in query for word in ['market cap', 'rank', 'volume'])
    }

    return {
        'coin': coin,
        'coin_ticker': coin_mapping.get(coin, ''),
        'query_types': [qt for qt, exists in query_types.items() if exists]
    }