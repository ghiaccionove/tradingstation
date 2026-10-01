import pandas as pd
from logger import logger

def get_market_category(market):
    '''
    restituisce la categoria di un mercato: 'stocks' oppure 'crypto'.
    Le azioni tokenizzate di Kraken (xStocks) hanno 'aclass_base' = 'tokenized_asset'.
    Per gli altri exchange questa informazione non c'è, quindi risulta 'crypto'.
    '''
    if market['info'].get('aclass_base') == 'tokenized_asset':
        return 'stocks'
    return 'crypto'

def get_request_params(exchange, symbol):
    '''
    parametri extra da aggiungere alle richieste di dati.
    Kraken vuole 'asset_class' quando si chiedono dati sulle azioni.
    '''
    market = exchange.ccxt.markets[symbol]
    if get_market_category(market) == 'stocks':
        return {'asset_class': 'tokenized_asset'}
    return {}

def fetch_market_data(exchange, symbol, timeframe='1m', limit=1000):
    logger.info('%s', symbol)
    params = get_request_params(exchange, symbol)
    data = pd.DataFrame(exchange.ccxt.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, params=params),
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return data

def fetch_symbols(exchange, market_type='spot', quote='USD', category='crypto'):
    '''
    restituisce la lista dei simboli dell'exchange che rispettano i filtri.
    market_type: 'spot', 'swap', 'future', ...
    quote: valuta di quotazione, es. 'USD', 'EUR', 'USDT'
    category: 'crypto', 'stocks' oppure 'all' (tutti)
    '''
    symbols = []
    for market in exchange.ccxt.markets.values():
        if market['type'] != market_type:
            continue
        if market['quote'] != quote:
            continue
        if market['active'] == False:
            continue
        if category != 'all' and get_market_category(market) != category:
            continue
        symbols.append(market['symbol'])
    return symbols

def filter_symbols_by_volume(exchange, symbols, min_volume=50000000):
    filtered_symbols = []
    for symbol in symbols:
        params = get_request_params(exchange, symbol)
        ticker = exchange.ccxt.fetch_ticker(symbol, params=params)
        volume = ticker['quoteVolume']
        if volume is None:  # alcuni mercati non hanno il dato del volume
            continue
        if volume >= min_volume:
            filtered_symbols.append(symbol)
    return filtered_symbols
