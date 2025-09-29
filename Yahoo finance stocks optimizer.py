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

print(get_stock_data("AAPL", "GOOG", "MC.PA").tail())


    