#Import Libraries 

import plotly.express as px
import numpy as np
import pandas as pd

# Function to plot an interactive plotly chart
def interactive_plot(df):
    fig = px.line(df, x='Date')
    for col in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[col], name=col)
    fig.update_layout(width=800, margin=dict(l=20, r=20, t=50, b=20), legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return fig

# Function to normalize the prices based on the initial price
def normalize(df):
    df_normalized = df.copy()
    for col in df_normalized.columns[1:]:
        df_normalized[col] = df_normalized[col] / df_normalized[col][0]
    return df_normalized

# Function to calculate daily returns
def daily_return(df):
    df_daily_return = df.copy()
    for col in df_daily_return.columns[1:]:
        df_daily_return[col] = (df_daily_return[col] - df_daily_return[col].shift(1)) / df_daily_return[col].shift(1) * 100
    df_daily_return.iloc[0, 1:] = 0
    return df_daily_return

# Function to calculate beta
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean() * 252
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a
