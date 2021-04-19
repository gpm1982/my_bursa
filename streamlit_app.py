# TODO: https://discuss.streamlit.io/t/stock-market-profile-chart/10751
import streamlit as st
import pandas as pd
import numpy as np

import gzip
import io
import urllib.request

title = 'MY Bursa Trading - Technical Analysis'
st.set_page_config(page_title=title, layout='wide')
st.title(title)

#DATE_COLUMN = 'date/time'
COUNTERS_URL = ('https://raw.githubusercontent.com/'
            'gpm1982/my_bursa/main/csv/counters.csv.gzip')
STOCKS_URL = ('https://raw.githubusercontent.com/'
            'gpm1982/my_bursa/main/csv/stocks.csv.gzip')

@st.cache
def load_counters():
    with urllib.request.urlopen(COUNTERS_URL) as url:
        url_f = io.BytesIO(url.read())
        gz = gzip.GzipFile(fileobj=url_f)

    data = pd.read_csv(gz)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data = data.set_index(['symbol'])
    return data

def load_stock_prices():
    with urllib.request.urlopen(STOCKS_URL) as url:
        url_f = io.BytesIO(url.read())
        gz = gzip.GzipFile(fileobj=url_f)

    data = pd.read_csv(gz)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data = data.set_index(['symbol'])
    return data

#data_load_state = st.text('Loading data...')
data = load_counters()
stock_prices = load_stock_prices()
#data_load_state.text("Done!")

#if st.checkbox('Show raw data'):
#    st.subheader('Raw data')
#    st.write(data)

stock_symbol = st.selectbox('Select Stock', data.index)
stock_info = data.loc[stock_symbol]
st.text("Technical Analysis for {0} ({1})".format(stock_info['corporatename'], stock_symbol))
stock_df = stock_prices.loc[stock_symbol]

st.subheader('Close Price with 200-day Moving Average')
chart_df = stock_df[['date', 'close', 'ma200']]
chart_df = chart_df.set_index(pd.DatetimeIndex(chart_df['date'].values))
chart_df = chart_df.drop(columns=['date'])
#st.write(chart_df)
st.line_chart(data=chart_df, width=0, height=0, use_container_width=True)

st.subheader('MACD')
chart_df = stock_df[['date', 'macd', 'signal line']]
chart_df = chart_df.set_index(pd.DatetimeIndex(chart_df['date'].values))
chart_df = chart_df.drop(columns=['date'])
#st.write(chart_df)
st.line_chart(data=chart_df, width=0, height=0, use_container_width=True)

st.subheader('Relative Strength Index (RSI)')
chart_df = stock_df[['date', 'rsi']]
chart_df = chart_df.set_index(pd.DatetimeIndex(chart_df['date'].values))
chart_df = chart_df.drop(columns=['date'])
#st.write(chart_df)
st.line_chart(data=chart_df, width=0, height=0, use_container_width=True)
