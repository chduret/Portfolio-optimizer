import yfinance as yf
import pandas as pd

user_input = input("Entrez les tickers (séparés par des virgules) : ")
tickers = [t.strip() for t in user_input.split(",") if t.strip()]

# Télécharger les données
data = yf.download(tickers, start="2020-01-01")["Close"]
print(data.tail())