import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fuzzywuzzy import process
from API_Fetch import get_stock_data
from ML import train_random_forest_model, predict_buy_sell_random_forest
from nasdaq_stock_list import load_nasdaq_tickers
from News_fetch import get_stock_news_from_newsapi

# Set page config
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

# Load NASDAQ tickers (cached)
nasdaq_stocks = load_nasdaq_tickers()

# Fuzzy search function
def get_ticker(company_name):
    best_match, score = process.extractOne(company_name, nasdaq_stocks.keys())
    return nasdaq_stocks[best_match] if score > 70 else None

# --- SIDEBAR FOR INPUTS ---
st.sidebar.header("🔍 Search & Filters")

company_name = st.sidebar.text_input("Company Name", "Apple Inc.", key="company_name_input")

ticker = get_ticker(company_name)

if ticker:
    period = st.sidebar.selectbox("Select Time Period", ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"], index=2)
    interval = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1d", "1wk", "1mo"], index=3)
    
    df = get_stock_data(ticker, period, interval)
    
    if df.empty:
        st.error("⚠️ No data found. Try another stock.")
    else:
        st.title(f"📈 {company_name} ({ticker}) Stock Performance")
        df["Date"] = pd.to_datetime(df["Date"])

        # Color logic
        last_close = df["Close"].iloc[-1]
        prev_close = df["Close"].iloc[-2] if len(df) > 1 else last_close
        color = "green" if last_close > prev_close else "red"

        # Displaying Stock Summary
        st.markdown(f"### **<span style='color:{color}'> 🔴🟢 {company_name} Stock Overview</span>**", unsafe_allow_html=True)
        st.write(f"📅 Latest Closing Price: **${last_close:.2f}**")
        st.write(f"📈 Previous Close: **${prev_close:.2f}**")

        # --- STOCK CHARTS ---
        col1, col2 = st.columns(2)

        # Candlestick Chart
        with col1:
            st.subheader("📊 Candlestick Chart")
            fig_candle = go.Figure()
            fig_candle.add_trace(go.Candlestick(
                x=df["Date"], open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                name="Candlestick"
            ))
            fig_candle.update_layout(
                xaxis_title="Date",
                yaxis_title="Stock Price (USD)",
                xaxis_rangeslider_visible=True,
                template="plotly_dark"
            )
            st.plotly_chart(fig_candle, use_container_width=True)

        # Line Chart
        with col2:
            st.subheader("📈 Line Chart")
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df["Date"], y=df["Close"],
                mode="lines", line=dict(color="cyan", width=2),
                name="Closing Price"
            ))
            fig_line.update_layout(
                xaxis_title="Date",
                yaxis_title="Stock Price (USD)",
                template="plotly_dark"
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # --- MACHINE LEARNING PREDICTION ---
        st.subheader("🔮 Buy/Sell Prediction")
        try:
            model, scaler = train_random_forest_model(df)
            prediction = predict_buy_sell_random_forest(df, model, scaler)
            st.markdown(f"### **📌 Prediction: `{prediction}`**")
        except Exception as e:
            st.error(f"⚠️ Error in training or prediction: {e}")

else:
    st.warning("⚠️ Stock not found. Try another company name.")

# Get stock ticker based on the company name from the sidebar

ticker = get_ticker(company_name)  # Dynamically get ticker for selected company

if company_name:
    news_articles = get_stock_news_from_newsapi(company_name, '')

    if news_articles:
        st.subheader(f"📰 Latest News for {company_name}")
        for idx, article in enumerate(news_articles, start=1):
            st.write(f"{idx}. **{article['title']}**")
            st.write(f"   *Publisher:* {article['publisher']}")
            st.write(f"   *Link:* [Read more]({article['link']})\n")
    else:
        st.write("No news available for this company.")
