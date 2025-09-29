### Web Scrapping - S&p 500 Historical Data Analysis

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as date

# Download historical data for S&P 500
data = yf.download('^GSPC', start='2000-01-01', end=date.datetime.today())
data = data['Close']
data = data.dropna()
data = pd.DataFrame(data)
data.columns = ['Close']
data['Return'] = data['Close'].pct_change()
data = data.dropna()
data['LogReturn'] = np.log(data['Close'] / data['Close'].shift(1))
data = data.dropna()
#Daily volatility
data['Daily_vol'] = data['LogReturn'].rolling(window=21).std()
data['Volatility'] = data['LogReturn'].rolling(window=21).std() * np.sqrt(252)  
data = data.dropna()
data['CumulativeReturn'] = (1 + data['Return']).cumprod() - 1
data = data.dropna()
data['CumulativeLogReturn'] = data['LogReturn'].cumsum()
data = data.dropna() 
print(data.head())

"""
We now have the close prices, daily returns, log returns, daily volatility, 
annualized volatility, cumulative returns, 
and cumulative log returns for the S&P 500 index from January 1, 2020, to January 1, 2023.
"""
print(data["2025-01-01":"2025-09-29"])
