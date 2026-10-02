import pandas as pd
from logger import logger
from config import MARKET_TYPE
from settings import TIMEFRAME, CANDLES_LIMIT, MIN_VOLUME

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

def fetch_market_data(exchange, symbol, timeframe=TIMEFRAME, limit=CANDLES_LIMIT):
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

def fetch_all_tickers(exchange, symbols):
    '''
    scarica i ticker (prezzo, volume, ...) di tutti i simboli con una sola richiesta,
    invece di una richiesta per simbolo.
    Su Kraken spot le azioni tokenizzate vanno chieste a parte, con il loro parametro:
    per questo i simboli vengono divisi in due gruppi.
    '''
    normal_symbols = []
    tokenized_symbols = []
    for symbol in symbols:
        if get_request_params(exchange, symbol) == {}:
            normal_symbols.append(symbol)
        else:
            tokenized_symbols.append(symbol)

    tickers = {}
    if len(normal_symbols) > 0:
        tickers.update(exchange.ccxt.fetch_tickers(normal_symbols))
    if len(tokenized_symbols) > 0:
        tickers.update(exchange.ccxt.fetch_tickers(tokenized_symbols, params={'asset_class': 'tokenized_asset'}))
    return tickers

def filter_symbols_by_volume(exchange, symbols, min_volume=MIN_VOLUME):
    filtered_symbols = []
    tickers = fetch_all_tickers(exchange, symbols)
    for symbol in symbols:
        if symbol not in tickers:  # nessun dato per questo simbolo
            continue
        volume = get_quote_volume(tickers[symbol])
        if volume is None:  # alcuni mercati non hanno il dato del volume
            continue
        if volume >= min_volume:
            filtered_symbols.append(symbol)
    return filtered_symbols

def count_active_candles(data, last_candles):
    '''quante delle ultime `last_candles` candele hanno avuto un movimento di prezzo (massimo diverso dal minimo)'''
    recent = data.tail(last_candles)
    moved = recent['high'] != recent['low']
    return int(moved.sum())
