import pandas as pd
import streamlit as st

@st.cache_data
def load_nasdaq_tickers():
    url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"
    df = pd.read_csv(url, sep="|")
    df = df[df["Nasdaq Traded"] == "Y"]
    return dict(zip(df["Security Name"], df["Symbol"]))
