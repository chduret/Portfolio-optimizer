### Web Scrapping - S&p 500 Historical Data Analysis

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as date
import scipy.stats as stats

def get_data():
    # Download historical data for S&P 500
    data = yf.download('^GSPC', start='2000-01-01', end=date.datetime.today())

    # Dowload risk free rate data (3-Month Treasury Bill and 10-Year Treasury Note)
    risk_free_3m = yf.download('^IRX', start='2000-01-01', end=date.datetime.today())
    risk_free_10 = yf.download('^TNX', start='2000-01-01', end=date.datetime.today())

    # Closing prices
    data = data['Close']
    data = data.dropna()

    # Convert to DataFrame
    data = pd.DataFrame(data)
    data.columns = ['Close']

    # Daily returns
    data['Return'] = data['Close'].pct_change()
    data = data.dropna()
    # Log returns
    data['LogReturn'] = np.log(data['Close'] / data['Close'].shift(1))
    data = data.dropna()
    #Daily volatility
    data['Daily_vol'] = data['LogReturn'].rolling(window=21).std()
    # Annualized volatility
    data['Volatility'] = data['LogReturn'].rolling(window=21).std() * np.sqrt(252)  
    data = data.dropna()
    # Cumulative returns
    data['CumulativeReturn'] = (1 + data['Return']).cumprod() - 1
    data = data.dropna()
    # Cumulative log returns
    data['CumulativeLogReturn'] = data['LogReturn'].cumsum()
    data = data.dropna() 

    # risk free rate
    data['RiskFree_3M'] = risk_free_3m['Close'] / 100
    data['RiskFree_10Y'] = risk_free_10['Close'] / 100
    data = data.dropna()

    """
    We now have the close prices, daily returns, log returns, daily volatility, 
    annualized volatility, cumulative returns, 
    and cumulative log returns for the S&P 500 index from January 1, 2020, to January 1, 2023.
    """
    # Calculate expected return 
    # Historical Expected Return
    data['Historical ER'] = data['LogReturn'].mean() * 252
    # Implied Expected Return with CAPM
    """
    CAPM =  Risk-Free Rate + Beta * (Market Return - Risk-Free Rate)
    """
    return data

print(get_data())