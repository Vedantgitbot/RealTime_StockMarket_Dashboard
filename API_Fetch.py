import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data
def get_stock_data(ticker, period="1mo", interval="1d"):
    """
    Fetch stock market data for a given ticker.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    return df
