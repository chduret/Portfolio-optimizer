### Web Scrapping - S&p 500 Historical Data Analysis

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download historical data for S&P 500
data = yf.download('^GSPC', start='2020-01-01', end='2023-01-01')
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