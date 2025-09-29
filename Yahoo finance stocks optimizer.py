import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as date
import scipy.stats as stats
import requests # To fetch the Wikipedia page

def get_stock_data(*tickers):
    start = "2000-01-01"
    end = date.datetime.now().strftime("%Y-%m-%d")
    
    data = yf.download(list(tickers), start=start, end=end, progress=False)
    data = data.dropna()
    
    return data

#Test
print(get_stock_data("AAPL", "GOOG", "MC.PA").tail())

def ann_ret(data):
    daily_returns = data['Adj Close'].pct_change().dropna()
    mean_daily_returns = daily_returns.mean()
    annualized_return = (1 + mean_daily_returns) ** 252 - 1
    return annualized_return

#Volatility using rolling window 
def ann_vol(data, window=63):
    daily_returns = data['Adj Close'].pct_change().dropna()
    rolling_volatility = daily_returns.rolling(window=window).std()
    annualized_rolling_volatility = rolling_volatility * np.sqrt(252)
    return annualized_rolling_volatility

def daily_vol(data, window=63):
    daily_returns = data['Adj Close'].pct_change().dropna()
    rolling_volatility = daily_returns.rolling(window=window).std()
    return rolling_volatility



