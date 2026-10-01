import time
from logger import logger
from utils.data_fetcher import fetch_symbols, filter_symbols_by_volume, fetch_market_data
from signals.votes import get_votes, decide, get_required_signals
from settings import PAUSE_SECONDS, TIMEFRAME, INDICATORS


def spotter(exchange, fetch_mode, category, pause_seconds=PAUSE_SECONDS):
    try:
        logger.info('Fetching symbols')
        symbols = fetch_symbols(exchange, category=category)
        logger.info('Simboli trovati: %s', len(symbols))
        if fetch_mode == 'volume':
            logger.info('Fetching most traded symbols')
            symbols = filter_symbols_by_volume(exchange, symbols)
            logger.info('Simboli dopo il filtro volume: %s', len(symbols))
        log_indicator_settings()
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
        votes = get_votes(data)
        direction, agreeing, enabled_count = decide(votes)
        if direction is not None:
            price = data['close'].iloc[-1]
            # warning = l'avviso arriva anche su Telegram
            logger.warning('%s su %s a %s - %s indicatori su %s (%s)',
                           direction, symbol, price, len(agreeing), enabled_count, ', '.join(agreeing))
        else:
            logger.debug('Voti su %s: %s', symbol, votes)
    except Exception as e:
        # info e non warning: i warning finiscono su Telegram, e non vogliamo
        # un messaggio per ogni errore. Il dettaglio completo va nel file di log.
        logger.info('Errore su %s, lo salto: %s', symbol, e)
        logger.debug('Dettaglio errore su %s', symbol, exc_info=True)


def log_indicator_settings():
    '''scrive all'avvio quali indicatori sono accesi e quanti ne servono per un avviso'''
    enabled = []
    for name, settings in INDICATORS.items():
        if settings['enabled']:
            enabled.append(name)
    required = get_required_signals(len(enabled))
    logger.info('Indicatori accesi: %s', ', '.join(enabled))
    logger.info("Avviso se almeno %s indicatori su %s sono d'accordo", required, len(enabled))
    if required > len(enabled):
        logger.info('ATTENZIONE: MIN_SIGNALS è più alto degli indicatori accesi, non arriverà nessun avviso')
