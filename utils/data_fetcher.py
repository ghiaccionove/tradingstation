import pandas as pd
from logger import logger

def fetch_market_data(exchange, symbol, timeframe='1m', limit=1000):
    logger.info('%s', symbol)
    data = pd.DataFrame(exchange.ccxt.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit),
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return data

def fetch_symbols(exchange, type='swap'):
    markets = pd.DataFrame(exchange.ccxt.fetch_markets())
    swap_symbols = markets.loc[(markets['type'] == type)&(markets['quoteId'] == 'USDT'), 'symbol']
    return swap_symbols

def filter_symbols_by_volume(exchange, symbols, min_volume=50000000):
    filtered_symbols = []
    for symbol in symbols:
            ticker = exchange.ccxt.fetch_ticker(symbol)
            volume = ticker.get('quoteVolume', 0)
            if volume >= min_volume:
                filtered_symbols.append(symbol)
    return filtered_symbols
