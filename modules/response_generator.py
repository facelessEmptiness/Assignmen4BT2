from openai import OpenAI
from config import OPENAI_API_KEY
import time

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
last_api_call = 0


def generate_response(context_data: dict) -> str:
    """Generate natural language response using OpenAI or fallback"""
    global last_api_call

    # Всегда сначала пробуем локальный генератор
    local_response = generate_local_response(context_data)

    # Если OpenAI недоступен, возвращаем локальный вариант
    if not client:
        return local_response

    # Проверяем квоту и тайминг
    try:
        current_time = time.time()
        if current_time - last_api_call < 1.0:  # Лимит 1 запрос в секунду
            time.sleep(1.0 - (current_time - last_api_call))

        prompt = build_prompt(context_data)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )

        last_api_call = time.time()
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"AI API error, using fallback: {str(e)}")
        return local_response


def build_prompt(context_data: dict) -> str:
    """Build the prompt for the AI"""
    news_titles = "\n".join([f"- {n['title']}" for n in context_data.get('news', [])[:3]])

    return f"""
    Provide a 2-sentence summary about {context_data.get('coin', 'the cryptocurrency')} using this data:
    - Price: ${context_data.get('price', 0):,.2f}
    - Market Cap: ${context_data.get('market_data', {}).get('market_cap', 0):,.2f}
    - Rank: #{context_data.get('market_data', {}).get('rank', 'N/A')}
    - 24h Change: {context_data.get('market_data', {}).get('price_change_24h', 0):.2f}%

    Recent News:
    {news_titles if news_titles else "No recent news"}

    Focus on the most interesting fact for a crypto investor.
    """


def generate_local_response(context_data: dict) -> str:
    """Generate response without OpenAI"""
    coin = context_data.get('coin', 'This cryptocurrency')
    price = context_data.get('price', 0)
    market_cap = context_data.get('market_data', {}).get('market_cap', 0)
    rank = context_data.get('market_data', {}).get('rank', 'N/A')
    change_24h = context_data.get('market_data', {}).get('price_change_24h', 0)

    news_summary = ""
    if context_data.get('news'):
        news_summary = f" Latest news: {context_data['news'][0]['title']}"

    return (
        f"{coin.capitalize()} is currently trading at ${price:,.2f} "
        f"(#{rank} by market cap at ${market_cap:,.2f}). "
        f"24h change: {change_24h:.2f}%.{news_summary}"
    )