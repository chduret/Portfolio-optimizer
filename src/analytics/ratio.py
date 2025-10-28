from src.data.volatility import volatility

# Sharpe Ratio
def sharpe_ratio(tickers, rf ):
    er = mu(tickers)
    vol = volatility(tickers)
    sharpe = (er - rf) / vol.iloc[-1]
    return sharpe

