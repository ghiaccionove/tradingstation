import time
from logger import logger
from utils.data_fetcher import select_symbols, fetch_market_data, count_active_candles
from signals.votes import get_votes, decide, get_required_signals
from settings import PROFILES


def spotter(exchange, profile_name):
    try:
        profile = PROFILES[profile_name]
        logger.info('Profilo: %s', profile_name)
        symbols = select_symbols(exchange, profile['filter'], profile['category'])
        log_indicator_settings(profile)
        logger.info('Searching for market condition (timeframe %s)', profile['timeframe'])
        # ultimo avviso inviato per ogni simbolo, es. {'BTC/USD:USD': ('LONG', 1790857020.5)}
        # (direzione e ora in secondi). Si azzera quando lo spotter viene riavviato.
        last_alerts = {}
        while True:
            skipped = 0
            for symbol in symbols:
                checked = check_symbol(exchange, symbol, profile, last_alerts)
                if checked == False:
                    skipped = skipped + 1
            logger.info('Giro completato: %s simboli controllati, %s saltati (senza dati, fermi o con errori)',
                        len(symbols) - skipped, skipped)
            # pausa tra un giro e l'altro, per non sovraccaricare l'exchange
            logger.info('Prossimo controllo tra %s secondi', profile['pause_seconds'])
            time.sleep(profile['pause_seconds'])
    except KeyboardInterrupt:
        logger.info('Spotter fermato')
    except Exception as e:
        logger.exception('Errore')


def check_symbol(exchange, symbol, profile, last_alerts):
    '''
    scarica i dati di un simbolo e applica la strategia del profilo.
    Restituisce True se il simbolo è stato controllato, False se è stato saltato.
    Se qualcosa va storto, lo segnala e prosegue: un errore su un solo simbolo
    non deve fermare tutto lo spotter.
    '''
    try:
        data = fetch_market_data(exchange, symbol, profile['timeframe'])
        if len(data) == 0:
            logger.debug('%s: nessuna candela, lo salto', symbol)
            return False
        active_candles = count_active_candles(data, profile['activity_candles'])
        if active_candles < profile['min_active_candles']:
            # mercato quasi fermo: gli indicatori darebbero segnali senza senso
            logger.debug('%s: solo %s candele con movimento nelle ultime %s, lo salto',
                         symbol, active_candles, profile['activity_candles'])
            return False
        votes = get_votes(data, profile['indicators'])
        direction, agreeing, enabled_count = decide(votes, profile['min_signals'])
        if direction is not None:
            if should_send_alert(last_alerts, symbol, direction, profile['alert_cooldown_minutes']):
                price = data['close'].iloc[-1]
                # warning = l'avviso arriva anche su Telegram
                logger.warning('%s su %s a %s - %s indicatori su %s (%s) [%s]',
                               direction, symbol, price, len(agreeing), enabled_count, ', '.join(agreeing),
                               profile['platform'])
                last_alerts[symbol] = (direction, time.time())
            else:
                logger.debug('%s su %s ancora attivo, avviso già inviato di recente', direction, symbol)
        else:
            logger.debug('Voti su %s: %s', symbol, votes)
        return True
    except Exception as e:
        # info e non warning: i warning finiscono su Telegram, e non vogliamo
        # un messaggio per ogni errore. Il dettaglio completo va nel file di log.
        logger.info('Errore su %s, lo salto: %s', symbol, e)
        logger.debug('Dettaglio errore su %s', symbol, exc_info=True)
        return False


def should_send_alert(last_alerts, symbol, direction, cooldown_minutes):
    '''
    decide se inviare l'avviso o se è una ripetizione. Si invia se:
    - è il primo avviso per questo simbolo, oppure
    - la direzione è cambiata rispetto all'ultimo avviso, oppure
    - sono passati almeno cooldown_minutes minuti dall'ultimo avviso
    '''
    if symbol not in last_alerts:
        return True
    last_direction, last_time = last_alerts[symbol]
    if direction != last_direction:
        return True
    minutes_passed = (time.time() - last_time) / 60
    return minutes_passed >= cooldown_minutes


def log_indicator_settings(profile):
    '''scrive all'avvio quali indicatori del profilo sono accesi e quanti ne servono per un avviso'''
    enabled = []
    for name, settings in profile['indicators'].items():
        if settings['enabled']:
            enabled.append(name)
    required = get_required_signals(len(enabled), profile['min_signals'])
    logger.info('Indicatori accesi: %s', ', '.join(enabled))
    logger.info("Avviso se almeno %s indicatori su %s sono d'accordo", required, len(enabled))
    logger.info('Lo stesso avviso non viene ripetuto prima di %s minuti', profile['alert_cooldown_minutes'])
    if required > len(enabled):
        logger.info('ATTENZIONE: min_signals è più alto degli indicatori accesi, non arriverà nessun avviso')
