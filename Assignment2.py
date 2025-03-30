import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title='🚀 Crypto Price Dashboard', page_icon=':chart_with_upwards_trend:', layout='wide')


def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

lottie_crypto = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_5ngs2ksb.json")

st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #1E1E1E;
            color: #e0e0e0;
            font-family: 'Montserrat', sans-serif;
        }
        .stMetric {
            background-color: #2C2C2C;
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3, h4, h5, h6 {
            color: #00ccff;
        }
        .stSidebar {
            background-color: #333333;
            padding: 20px;
            border-radius: 15px;
        }
        .stButton > button {
            background-color: #00ccff;
            color: #ffffff;
            border-radius: 10px;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #0099cc;
        }
    </style>
""", unsafe_allow_html=True)

st_lottie(lottie_crypto, speed=1, height=200, key="crypto")
st.title('🚀 Crypto Price Dashboard')
st.markdown('### Real-time crypto prices & trends')

st.sidebar.header('Select Cryptocurrency')
crypto_options = ['bitcoin', 'ethereum', 'ripple', 'dogecoin', 'litecoin', 'cardano', 'polkadot', 'solana', 'avalanche', 'binancecoin', 'chainlink', 'stellar', 'monero', 'vechain', 'tron']
selected_crypto = st.sidebar.selectbox('Choose a cryptocurrency:', crypto_options)

def fetch_price_data(crypto):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true'
    response = requests.get(url)
    data = response.json()
    try:
        price = data[crypto]['usd']
        market_cap = data[crypto]['usd_market_cap']
        change_24h = data[crypto]['usd_24h_change']
        return price, market_cap, change_24h
    except (KeyError, TypeError):
        st.error("Failed to fetch current data. Please try again later.")
        return None, None, None

current_price, market_cap, change_24h = fetch_price_data(selected_crypto)

if current_price is not None and market_cap is not None:
    st.markdown(f'## 📈 {selected_crypto.capitalize()} Statistics')
    col1, col2, col3 = st.columns(3)
    col1.metric(label='💰 Current Price (USD)', value=f'${current_price:,}')
    col2.metric(label='🏷️ Market Cap (USD)', value=f'${market_cap:,.0f}')
    col3.metric(label='🔺 24h Change (%)', value=f'{change_24h:.2f}%')

def fetch_historical_data(crypto):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=30&interval=daily'
    response = requests.get(url)
    data = response.json()
    try:
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
        df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
        return df[['Date', 'Price']]
    except (KeyError, TypeError):
        st.error("Failed to fetch historical price data. Please try again later.")
        return pd.DataFrame()

hist_data = fetch_historical_data(selected_crypto)
if not hist_data.empty:
    fig = px.line(hist_data, x='Date', y='Price', title=f'{selected_crypto.capitalize()} Price Trend (Last 30 Days)', line_shape='spline', markers=True, template='plotly_dark', color_discrete_sequence=['#00ccff'])
    st.plotly_chart(fig)

st.caption('🔗 Data from CoinGecko API')
