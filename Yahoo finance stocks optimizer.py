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

def ann_vol(data):
    daily_returns = data['Adj Close'].pct_change().dropna()
    daily_volatility = daily_returns.std()
    annualized_volatility = daily_volatility * np.sqrt(252)
    return annualized_volatility

def daily_vol(data):
    daily_returns = data['Adj Close'].pct_change().dropna()
    daily_volatility = daily_returns.std()
    return daily_volatility

