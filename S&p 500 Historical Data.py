### Web Scrapping - S&p 500 Historical Data Analysis
install pandas numpy matplotlib yfinance 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download historical data for S&P 500
data = yf.download('^GSPC', start='2020-01-01', end='2023-01-01')
data = data['Adj Close']
data = data.dropna()
data = data.to_frame()
data.columns = ['Close']
data['Return'] = data['Close'].pct_change()
data = data.dropna()
data['LogReturn'] = np.log(data['Close'] / data['Close'].shift(1))
data = data.dropna()
data['Volatility'] = data['LogReturn'].rolling(window=21).std() * np.sqrt(252)  
data = data.dropna()
data['CumulativeReturn'] = (1 + data['Return']).cumprod() - 1
data = data.dropna()
data['CumulativeLogReturn'] = data['LogReturn'].cumsum()
data = data.dropna()

print(data.head())