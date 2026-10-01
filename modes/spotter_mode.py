import time
from logger import logger
from utils.data_fetcher import fetch_symbols, filter_symbols_by_volume, fetch_market_data
from strategies.base_strategy import Valubot
from settings import PAUSE_SECONDS, TIMEFRAME


def spotter(exchange, fetch_mode, category, pause_seconds=PAUSE_SECONDS):
    try:
        logger.info('Fetching symbols')
        symbols = fetch_symbols(exchange, category=category)
        logger.info('Simboli trovati: %s', len(symbols))
        if fetch_mode == 'volume':
            logger.info('Fetching most traded symbols')
            symbols = filter_symbols_by_volume(exchange, symbols)
            logger.info('Simboli dopo il filtro volume: %s', len(symbols))
        logger.info('Searching for market condition (timeframe %s)', TIMEFRAME)
        while True:
            for symbol in symbols:
                check_symbol(exchange, symbol)
            # pausa tra un giro e l'altro, per non sovraccaricare l'exchange
            logger.info('Giro completato, prossimo controllo tra %s secondi', pause_seconds)
            time.sleep(pause_seconds)
    except KeyboardInterrupt:
        logger.info('Spotter fermato')
    except Exception as e:
        logger.exception('Errore')


def check_symbol(exchange, symbol):
    '''
    scarica i dati di un simbolo e applica la strategia.
    Se qualcosa va storto, lo segnala e prosegue: un errore su un solo simbolo
    non deve fermare tutto lo spotter.
    '''
    try:
        data = fetch_market_data(exchange, symbol)
        Valubot(data, exchange).generate_signal(symbol)
    except Exception as e:
        # info e non warning: i warning finiscono su Telegram, e non vogliamo
        # un messaggio per ogni errore. Il dettaglio completo va nel file di log.
        logger.info('Errore su %s, lo salto: %s', symbol, e)
        logger.debug('Dettaglio errore su %s', symbol, exc_info=True)
