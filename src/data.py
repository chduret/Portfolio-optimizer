import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as date
import scipy.stats as stats

def get_prices(tickers, start="2000-01-01", end=None):
    if end is None:
        end=date.datetime.today()
    
    prices = yf.download(tickers, start=start, end=end)["Close"]

    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name="Close")
    
    prices = prices.dropna()
    return prices

def get_risk_free(start="2000-01-01", end=None):
    if end is None:
        end = date.datetime.today()

    rf_3m = yf.download("^IRX", start=start, end=end)["Close"] / 100
    rf_10y = yf.download("^TNX", start=start, end=end)["Close"] / 100

    risk_free = pd.DataFrame({"RiskFree_3M": rf_3m, "RiskFree_10Y": rf_10y})
    risk_free = risk_free.dropna()
    return risk_free


def get_data(tickers):
    # Download historical data for S&P 500
    data = yf.download(tickers, start='2000-01-01', end=date.datetime.today())

    # Dowload risk free rate data (3-Month Treasury Bill and 10-Year Treasury Note)
    risk_free_3m = yf.download('^IRX', start='2000-01-01', end=date.datetime.today())
    risk_free_10 = yf.download('^TNX', start='2000-01-01', end=date.datetime.today())

    # Closing prices
    data = data['Close']

   # If it's a Series (single ticker), make it a DataFrame with a nice name
    if isinstance(data, pd.Series):
        data = data.to_frame(name="Close")

    data = data.dropna()


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

user_input = input("Entrez les tickers (séparés par des virgules) : ")
tickers = [t.strip() for t in user_input.split(",") if t.strip()]


SP500 = get_prices(tickers=tickers)

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

