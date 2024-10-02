import pandas as pd

def fetch_market_data(exchange, symbol, timeframe='1m', limit=1000):
    data = pd.DataFrame(exchange.ccxt.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit),
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return data

def fetch_symbols(exchange, type='swap'):
    markets = pd.DataFrame(exchange.ccxt.fetch_markets())
    swap_symbols = markets.loc[(markets['type'] == type)&(markets['quoteId'] == 'USDT'), 'symbol']
    return swap_symbols