# calculated_beta.py
import pandas as pd
import numpy as np

def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean() * 252
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a

def calculate_all_betas(stocks_daily_return, stock_list):
    beta_dict = {}
    for stock in stock_list:
        beta, alpha = calculate_beta(stocks_daily_return, stock)
        beta_dict[stock] = {'beta': beta, 'alpha': alpha}
    return beta_dict
