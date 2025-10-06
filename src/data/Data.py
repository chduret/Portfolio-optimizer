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

    risk_free = pd.Series({"RiskFree_3M": rf_3m, "RiskFree_10Y": rf_10y})
    risk_free = risk_free.dropna()
    return risk_free

def returns(ticker):
    returns = get_prices(ticker).pct_change().dropna()
    return returns

# Annual vol on 63 days (quarter)
def volatility(tickers, window=63):
    returns_data = returns(tickers)
    vol = returns_data.rolling(window=window).std() * np.sqrt(252)
    return vol

#Daily vol on 63 days (quarter)
def daily_vol(tickers, window=63):
    returns_data= returns(tickers)
    daily_vol = returns_data.rolling(window=window).std() 
    return daily_vol

#Test
#ticker = ["AAPL", "GOOG", "MC.PA"]
#print(returns(ticker).tail())

# Matrice de corrélation
def correlation_matrix(tickers):
    returns_data = returns(tickers)
    corr_matrix = returns_data.corr()
    return corr_matrix

# Matrice de covariance
def covariance_matrix(tickers):
    returns_data = returns(tickers)
    cov_matrix = returns_data.cov()
    return cov_matrix

# Annualized expected returns
def mu(tickers):
    returns_data = returns(tickers)
    mean_returns = returns_data.mean() * 252  # Annualized mean return
    return mean_returns

# Daily expected returns
def day_mu(tickers):
    returns_data = returns(tickers)
    mean_returns = returns_data.mean()
    return mean_returns

risk_free = get_risk_free()

def sharpe_ratio(tickers, rf ):
    er = mu(tickers)
    vol = volatility(tickers)
    sharpe = (er - rf) / vol.iloc[-1]
    return sharpe

# Quick test

"""
if __name__ == "__main__":
    print("Running quick test…", flush=True)  # prints immediately
    tickers = ["AAPL", "MSFT", "TSLA"]

    px = get_prices(tickers, start="2025-05-01")
    print("\nPrices (tail):")
    print(px.tail(), flush=True)

    rets = returns(tickers)
    print("\nReturns (tail):")
    print(rets.tail(), flush=True)

    vol = volatility(tickers, window=10)
    print("\nVolatility (10d annualized, tail):")
    print(vol.tail(), flush=True)

    corr = correlation_matrix(tickers)
    print("\nCorrelation matrix:")
    print(corr)

    """



