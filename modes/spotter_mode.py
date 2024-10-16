from logger import logger
from utils.data_fetcher import *
from signals.signals_generator import *
from strategies.base_strategy import Valubot


def spotter(exchange, fetch):
    try:
        logger.info('Fetching symbols')
        symbols = fetch_symbols(exchange)
        if fetch == 'volume':
            logger.info('Fetching most traded symbols')
            symbols = filter_symbols_by_volume(exchange, symbols)
        logger.info('Searching for market condition')
        while True:
            for symbol in symbols:
                data = fetch_market_data(exchange, symbol)
                Valubot(data, exchange).generate_signal(symbol)
    except Exception as e:
        logger.exception('Errore')