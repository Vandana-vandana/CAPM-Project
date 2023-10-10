# Import libraries

import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
from pages.calculated_beta import calculate_all_betas
from capm_function import interactive_plot, normalize, daily_return

st.set_page_config(page_title="CAPM", page_icon="chart_with_upwards_trend", layout="wide")
st.title("Capital Asset Pricing Model")

# Getting input from the user
col1, col2 = st.columns((1, 1))
with col1:
    stock_list = st.multiselect("Choose 4 stocks", ["TSLA", "AAPL", "NFLX", "MSFT", "MGM", "AMZN", "NVEA", "GOOGL"], ["TSLA", "AAPL", "AMZN", "GOOGL"])
with col2:
    year = st.number_input("Number of years", 1, 10)

# Downloading data for S&P 500
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
    sp500 = web.DataReader('sp500', 'fred', start, end)

    stocks_df = pd.DataFrame()

    for stock in stock_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df[f'{stock}'] = data['Close']

    stocks_df.reset_index(inplace=True)
    sp500.reset_index(inplace=True)
    sp500.columns = ['Date', 'sp500']

    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df, sp500, on='Date', how='inner')

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all the stocks")
        st.plotly_chart(interactive_plot(stocks_df))
    with col2:
        st.markdown("### Price of all the stocks (After Normalization)")
        st.plotly_chart(interactive_plot(normalize(stocks_df)))

    stocks_daily_return = daily_return(stocks_df)

    beta_dict = calculate_all_betas(stocks_daily_return, stock_list)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Calculated Beta Values')
        st.write(beta_dict)

    rf = 0
    rm = stocks_daily_return['sp500'].mean() * 252

    return_df = pd.DataFrame({'Stock': stock_list, 'Return Value': [round(rf + (beta_dict[stock]['beta'] * (rm - rf)), 2) for stock in stock_list]})

    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df, use_container_width=True)

except Exception as e:
    st.write(f"Please select valid input. An error occurred: {e}")
