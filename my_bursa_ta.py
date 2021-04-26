# TODO: https://discuss.streamlit.io/t/stock-market-profile-chart/10751
# Using Google Drive API via Service Account: https://dev.to/ajeebkp23/google-drive-api-access-via-service-account-python-33le
import streamlit as st
import datetime as dt
import pandas as pd
import numpy as np

import io
import gzip
import json
import logging
import urllib.request

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from apiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials

# Suppress INFO messages from displaying in website
logging.getLogger('oauth2client.transport').setLevel(logging.ERROR)
logging.getLogger('oauth2client.client').setLevel(logging.ERROR)

# Title of the website
title = 'MY Bursa Trading - Technical Analysis'
st.set_page_config(page_title=title, layout='wide')
st.title(title)

# https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py
key_dict = json.loads(st.secrets["gdrive_key"])
scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scopes=scopes)

# https://developers.google.com/drive/api/v3/quickstart/python
service = build('drive', 'v3', credentials=credentials, cache_discovery=False)

@st.cache
def get_csv_to_pd (file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        #print("Download %d%%." % int(status.progress() * 100))

    fh.seek(0)
    gz = gzip.GzipFile(fileobj=fh)
    data = pd.read_csv(gz)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data = data.set_index(['symbol'])
    return data

# Do not change these IDs unless the ID has changed
STOCKS_INFO = '1k6LJ8hTCDnFXttuu_vH9Li7VhqY6f4Ou'
STOCK_PRICES = '1O-pXLZKGNcLlP3entttVVHAUjQGaIsYw'

# Load data from Google Drive
stocks_info=get_csv_to_pd(STOCKS_INFO)
stock_prices=get_csv_to_pd(STOCK_PRICES)

# Sidebar Options
stock_symbol = st.sidebar.selectbox('Select Stock', stocks_info.index)
stock_info = stocks_info.loc[stock_symbol]
ema = st.sidebar.checkbox('Show EMA')
macd = st.sidebar.checkbox('Show MACD')
rsi = st.sidebar.checkbox('Show RSI')

# Populate data for selected stocks
st.text("Technical Analysis for {0} ({1})".format(stock_info['corporatename'], stock_symbol))
stock_df = stock_prices.loc[stock_symbol]
stock_df = stock_df.set_index(pd.DatetimeIndex(stock_df['date'].values))
stock_df = stock_df.drop(columns=['date'])

#st.subheader('Stock Price with 200-day Moving Average')
# Preparing area for displaying stock market data
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    horizontal_spacing = 0.01,
    vertical_spacing = 0.01
)

# Candlestick graph
dateStr = stock_df.index.strftime("%d-%m-%Y")
fig.add_trace(
    go.Candlestick(x=dateStr,
            open=stock_df['open'],
            high=stock_df['high'],
            low=stock_df['low'],
            close=stock_df['close'],
            yaxis= "y2",
            name="Price"
    ),
    row=1, col=1
)

# MA200 line together with candlestick
fig.add_trace(
    go.Scatter(
        x=dateStr,
        y=stock_df['ma200'],
        mode="lines",
        name="MA200",
        line=dict(
            color="yellow"
        )
    )
)

# Volume chart
fig.add_trace(
    go.Bar(
        x=dateStr,
        y=stock_df['volume'],
        name="Volume"
    ),
    row=2, col=1
)

fig.update_layout(
    showlegend=False,
    height=700,
    xaxis_rangeslider_visible=False,
    title_text="Stock Price with 200-day Moving Average"
)

config={
    'modeBarButtonsToAdd': ['drawline']
}

st.plotly_chart(fig, use_container_width=True, config=config)

if ema:
    # Prepare second set of charts for EMA technical analysis
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        horizontal_spacing = 0.01,
        vertical_spacing = 0.01
    )

    # Let's display EMA (S=12, L=26)
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['close'],
            name="Close"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['ema12'],
            name="EMA12"
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['ema26'],
            name="EMA26"
        ),
        row=2, col=1
    )

    fig.update_layout(
        showlegend=False,
        height=700,
        title_text="Exponential Moving Average (Short=12d, Long=26d)"
    )

    st.plotly_chart(fig, use_container_width=True, config=config)

if macd:
    # Prepare second set of charts for MACD technical analysis
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        horizontal_spacing = 0.01,
        vertical_spacing = 0.01
    )

    # Let's display MACD (S=12, L=26, EMA=9)
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['close'],
            name="Close"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['macd'],
            name="MACD"
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['signal line'],
            name="Signal Line"
        ),
        row=2, col=1
    )

    fig.update_layout(
        showlegend=False,
        height=700,
        title_text="Moving Average Convergence Divergence (Short=12d, Long=26d, EMA=9d)"
    )

    st.plotly_chart(fig, use_container_width=True, config=config)

if rsi:
    # Prepare second set of charts for RSI technical analysis
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        horizontal_spacing = 0.01,
        vertical_spacing = 0.01
    )

    # Let's display RSI (Period=14d)
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['close'],
            name="Close"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Line(
            x=dateStr,
            y=stock_df['rsi'],
            name="RSI"
        ),
        row=2, col=1
    )

    fig.update_layout(
        showlegend=False,
        height=700,
        title_text="Relative Strength Index (Period=14d)"
    )

    st.plotly_chart(fig, use_container_width=True, config=config)