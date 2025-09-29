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

    # Calcul du beta 
    """
    Beta can be calculated historically for all the periods or using a rolling window.
    rolling window is more relevant as it captures the changing dynamics of the market.
    A common choice is a 1-year rolling window (252 trading days) or 5 years (1260 trading days). 
    """
    # 1-year rolling window beta
    beta_1y = data['LogReturn'].rolling(window=252).cov() / data['LogReturn'].rolling(window=252).var()

    """
    We now have the close prices, daily returns, log returns, daily volatility, 
    annualized volatility, cumulative returns, 
    and cumulative log returns for the S&P 500 index from January 1, 2020, to January 1, 2023.
    """
    # CALCULATE EXPECTED RETURN

    # Historical Expected Return
    data['mu histo'] = data['LogReturn'].mean() * 252
    # Implied Expected Return with CAP
    """
    CAPM =  Risk-Free Rate + Beta * (Market Return - Risk-Free Rate)
    
    """

    return data

SP500 = get_data()

#Save to CSV-file :
#SP500.to_csv('SP500_Historical_Data.csv')

#Plot returns from xdate to ydate
"""
SP500["Return"]["2023-01-03":"2025-09-29"].plot(title="S&P 500 Daily Returns (2023-2025)", figsize=(10, 6))
# Plot settings - not necessary
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.grid()

#plt.show() to display the plot
plt.show()
"""

