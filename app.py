import streamlit as st
from main import crypto_assistant
from config import COINMARKETCAP_API_KEY, CRYPTO_PANIC_API_KEY
import time

# Настройка страницы
st.set_page_config(
    page_title="AI Crypto Assistant",
    page_icon="💰",
    layout="centered"
)

# CSS стили
st.markdown("""
<style>
    /* Основные стили */
    .stTextInput input {
        font-size: 18px !important;
    }
    .stButton button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
    }

    /* Стили для блока ответа */
    .response-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-top: 20px;
        border-left: 5px solid #4CAF50;
    }
    .response-box h3 {
        color: #333333 !important;
        margin-top: 0 !important;
    }
    .response-box p {
        color: #000000 !important;  /* Черный цвет текста */
        font-size: 16px !important;
        line-height: 1.6 !important;
        margin-bottom: 10px !important;
    }
    .response-box .meta {
        font-size: 14px !important;
        color: #666666 !important;
    }

    /* Улучшение читаемости основного текста */
    body {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Заголовок приложения
st.title("💰 AI Crypto Assistant")
st.markdown("Get real-time cryptocurrency data with AI-powered insights")


# Проверка API ключей
def check_api_keys():
    if not COINMARKETCAP_API_KEY or not CRYPTO_PANIC_API_KEY:
        st.warning("⚠️ Please configure API keys in config.py")
        st.stop()


# Основной интерфейс
def main():
    check_api_keys()

    with st.form("query_form"):
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_input(
                "Ask about any cryptocurrency:",
                placeholder="e.g. What's happening with Bitcoin?",
                key="query_input"
            )
        with col2:
            submit_button = st.form_submit_button("Ask", type="primary")

    if submit_button and query:
        with st.spinner("Fetching data and generating response..."):
            start_time = time.time()

            # Получаем ответ от ассистента
            response = crypto_assistant(query)

            execution_time = time.time() - start_time

            # Показываем ответ
            st.markdown(f"""
            <div class="response-box">
                <h3>📊 Response</h3>
                <p>{response}</p>
                <p style="font-size: 0.8em; color: #666;">
                    Generated in {execution_time:.2f} seconds
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Показываем примеры запросов
            st.markdown("""
            **💡 Try these examples:**
            - What's the latest news about Ethereum?
            - Tell me about Solana's price and market cap
            - How is Bitcoin performing today?
            """)


if __name__ == "__main__":
    main()