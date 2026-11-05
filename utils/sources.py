'''
Da dove arrivano i dati: sceglie tra Kraken (ccxt) e Yahoo in base al profilo ('source').
Spotter ed evaluate usano solo queste funzioni, così non devono sapere quale fonte è attiva.
'''
from logger import logger
from settings import CANDLES_LIMIT
from utils.data_fetcher import select_symbols, fetch_market_data, fetch_history
from utils.yahoo_fetcher import fetch_yahoo_data, fetch_yahoo_history

def get_symbols(exchange, profile):
    '''simboli da controllare: su Kraken si scelgono con i filtri, su Yahoo sono la watchlist del profilo'''
    if profile['source'] == 'yahoo':
        logger.info('Simboli dalla watchlist: %s', len(profile['symbols']))
        return profile['symbols']
    return select_symbols(exchange, profile['filter'], profile['category'])

def get_candles(exchange, symbol, profile):
    '''ultime candele di un simbolo (l'ultima può essere ancora in corso)'''
    if profile['source'] == 'yahoo':
        return fetch_yahoo_data(symbol, profile['timeframe'], CANDLES_LIMIT)
    return fetch_market_data(exchange, symbol, profile['timeframe'])

def get_history(exchange, symbol, total_candles, profile):
    '''storico di candele chiuse, per la valutazione'''
    if profile['source'] == 'yahoo':
        return fetch_yahoo_history(symbol, total_candles, profile['timeframe'])
    return fetch_history(exchange, symbol, total_candles, profile['timeframe'])
