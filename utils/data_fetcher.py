import pandas as pd
from logger import logger
from config import MARKET_TYPE

# Categorie di Kraken Futures che consideriamo mercati tradizionali ('tradfi').
# Tutte le altre (DeFi, Meme, AI, Layer 1, ...) sono considerate 'crypto'.
TRADFI_CATEGORIES = ['xStocks', 'Equities', 'Indices', 'Pre-IPO', 'Commodities', 'Forex']

def get_market_category(market):
    '''
    restituisce la categoria di un mercato: 'tradfi' (mercati tradizionali:
    azioni, indici, materie prime, valute) oppure 'crypto'.
    Per gli exchange che non danno questa informazione risulta sempre 'crypto'.
    '''
    info = market['info']
    # Kraken spot: le azioni tokenizzate (xStocks) hanno aclass_base = 'tokenized_asset'
    if info.get('aclass_base') == 'tokenized_asset':
        return 'tradfi'
    # Kraken Futures: ogni mercato ha un campo 'category'
    if info.get('category') in TRADFI_CATEGORIES:
        return 'tradfi'
    return 'crypto'

def get_request_params(exchange, symbol):
    '''
    parametri extra da aggiungere alle richieste di dati.
    Kraken spot vuole 'asset_class' quando si chiedono dati sulle azioni tokenizzate.
    '''
    market = exchange.ccxt.markets[symbol]
    if market['info'].get('aclass_base') == 'tokenized_asset':
        return {'asset_class': 'tokenized_asset'}
    return {}

def fetch_market_data(exchange, symbol, timeframe='1m', limit=1000):
    logger.info('%s', symbol)
    params = get_request_params(exchange, symbol)
    data = pd.DataFrame(exchange.ccxt.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, params=params),
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return data

def fetch_symbols(exchange, market_type=MARKET_TYPE, quote='USD', category='crypto'):
    '''
    restituisce la lista dei simboli dell'exchange che rispettano i filtri.
    market_type: 'swap' (perpetual), 'spot', 'future', ... (predefinito: MARKET_TYPE in config.py)
    quote: valuta di quotazione, es. 'USD', 'EUR', 'USDT'
    category: 'crypto', 'tradfi' oppure 'all' (tutti)
    '''
    symbols = []
    for market in exchange.ccxt.markets.values():
        if market['type'] != market_type:
            continue
        if market['quote'] != quote:
            continue
        if market['active'] == False:
            continue
        # contratti inversi (regolati in crypto, es. BTC/USD:BTC): li escludiamo
        if market['inverse'] == True:
            continue
        if category != 'all' and get_market_category(market) != category:
            continue
        symbols.append(market['symbol'])
    return symbols

def get_quote_volume(ticker):
    '''
    volume delle ultime 24 ore in valuta di quotazione (es. dollari).
    Alcuni exchange (es. Kraken Futures) non lo forniscono direttamente:
    in quel caso lo calcoliamo come volume in monete * ultimo prezzo.
    '''
    if ticker['quoteVolume'] is not None:
        return ticker['quoteVolume']
    if ticker['baseVolume'] is not None and ticker['last'] is not None:
        return ticker['baseVolume'] * ticker['last']
    return None

def filter_symbols_by_volume(exchange, symbols, min_volume=50000000):
    filtered_symbols = []
    for symbol in symbols:
        params = get_request_params(exchange, symbol)
        ticker = exchange.ccxt.fetch_ticker(symbol, params=params)
        volume = get_quote_volume(ticker)
        if volume is None:  # alcuni mercati non hanno il dato del volume
            continue
        if volume >= min_volume:
            filtered_symbols.append(symbol)
    return filtered_symbols
