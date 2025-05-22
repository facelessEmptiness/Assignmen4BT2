from modules.query_parser import parse_user_query
from modules.news_client import get_crypto_news
from modules.exchange_client import get_current_price
from modules.market_client import get_market_data
from modules.response_generator import generate_response
from utils.coin_mapping import get_coin_metadata
import streamlit as st


def crypto_assistant(query: str) -> str:
    """Main function to handle user queries"""
    # Parse the user query
    parsed = parse_user_query(query)
    if not parsed['coin']:
        return "Sorry, I couldn't identify a cryptocurrency in your query."

    # Get coin metadata
    coin_meta = get_coin_metadata(parsed['coin'])
    if not coin_meta:
        return f"Sorry, I don't have data for {parsed['coin']}."

    # Display progress in Streamlit
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Fetch all required data with progress updates
    context = {'user_query': query, 'coin': parsed['coin']}

    status_text.text("Fetching price data...")
    context['price'] = get_current_price(coin_meta['ticker'])
    progress_bar.progress(25)

    status_text.text("Fetching market data...")
    context['market_data'] = get_market_data(coin_meta['coinmarketcap_id'])
    progress_bar.progress(50)

    status_text.text("Fetching latest news...")
    context['news'] = get_crypto_news(coin_meta['cryptopanic_id'])
    progress_bar.progress(75)

    status_text.text("Generating AI response...")
    response = generate_response(context)
    progress_bar.progress(100)

    status_text.empty()
    progress_bar.empty()

    return response