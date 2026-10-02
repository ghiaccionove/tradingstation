'''
Modalità 'evaluate': valuta i segnali sui dati storici.

Scorre la storia candela per candela vedendo solo il passato, esattamente come farebbe
lo spotter dal vivo (stessi voti, stessa finestra di candele, stesso filtro sui mercati
fermi, stesso blocco degli avvisi ripetuti). Per ogni segnale misura cosa ha fatto il
prezzo dopo alcune candele e lo confronta con l'entrare "a caso" nella stessa direzione.
'''
import os
import time
import pandas as pd
from logger import logger
from utils.data_fetcher import select_symbols, fetch_history, count_active_candles
from signals.votes import get_votes, decide
from signals.signal_types import Signal
from signals.indicators import get_candle_minutes
from modes.spotter_mode import log_indicator_settings
from settings import TIMEFRAME, CANDLES_LIMIT, ACTIVITY_CANDLES, MIN_ACTIVE_CANDLES, ALERT_COOLDOWN_MINUTES
from settings import EVAL_CANDLES, EVAL_HORIZONS, EVAL_FEE_PERCENT

# candele iniziali da non valutare: servono agli indicatori per "scaldarsi"
WARMUP_CANDLES = 200

# sotto questo numero di segnali il risultato è poco affidabile
MIN_RELIABLE_SIGNALS = 30

# cartella dove salvare l'elenco dei segnali (esclusa da git)
RESULTS_FOLDER = 'evaluations'


def evaluate(exchange, fetch_mode, category):
    try:
        symbols = select_symbols(exchange, fetch_mode, category)
        log_indicator_settings()
        logger.info('Valutazione su %s candele da %s per simbolo', EVAL_CANDLES, TIMEFRAME)
        all_signals = []
        all_candles = []   # tutte le candele valutate, per il confronto "a caso"
        number = 0
        for symbol in symbols:
            number = number + 1
            logger.info('[%s/%s] %s', number, len(symbols), symbol)
            try:
                data = fetch_history(exchange, symbol, EVAL_CANDLES)
                signals, candles = evaluate_symbol(data, symbol)
                all_signals = all_signals + signals
                all_candles = all_candles + candles
            except Exception as e:
                logger.info('Errore su %s, lo salto: %s', symbol, e)
        signals_table = pd.DataFrame(all_signals)
        candles_table = pd.DataFrame(all_candles)
        print_report(signals_table, candles_table)
        save_signals(signals_table)
    except KeyboardInterrupt:
        logger.info('Valutazione interrotta')


def price_change_percent(closes, t, candles_after):
    '''di quanto è cambiato il prezzo, in %, dalla candela t a `candles_after` candele dopo'''
    return (closes.iloc[t + candles_after] / closes.iloc[t] - 1) * 100


def evaluate_symbol(data, symbol):
    '''
    scorre la storia di un simbolo e restituisce due elenchi:
    - signals: i segnali trovati, con il risultato dopo ogni orizzonte (al netto delle commissioni)
    - candles: tutte le candele valutate, con la variazione di prezzo (serve per il confronto "a caso")
    '''
    signals = []
    candles = []
    if len(data) < WARMUP_CANDLES + max(EVAL_HORIZONS) + 1:
        logger.info('%s: storico troppo corto, lo salto', symbol)
        return signals, candles

    closes = data['close']
    cooldown_candles = ALERT_COOLDOWN_MINUTES / get_candle_minutes(data)
    last_direction = None
    last_index = None
    # ci servono candele "future" per misurare il risultato: ci fermiamo prima della fine
    last_t = len(data) - max(EVAL_HORIZONS)
    # la storia viene divisa a metà in due periodi
    middle = (WARMUP_CANDLES + last_t) // 2

    for t in range(WARMUP_CANDLES, last_t):
        if t < middle:
            period = 1
        else:
            period = 2
        candle_time = pd.to_datetime(data['timestamp'].iloc[t], unit='ms')
        # le ultime candele fino a t, come le vedrebbe lo spotter in quel momento
        window = data.iloc[max(0, t + 1 - CANDLES_LIMIT):t + 1]
        if count_active_candles(window, ACTIVITY_CANDLES) < MIN_ACTIVE_CANDLES:
            continue   # mercato fermo: lo spotter lo salterebbe

        # ogni candela valutata serve al confronto "a caso"
        candle = {'time': candle_time, 'period': period}
        for h in EVAL_HORIZONS:
            candle[f'change_{h}'] = price_change_percent(closes, t, h)
        candles.append(candle)

        direction, agreeing, enabled_count = decide(get_votes(window))
        if direction is None:
            continue
        # blocco degli avvisi ripetuti, come nello spotter
        if direction == last_direction and t - last_index < cooldown_candles:
            continue
        last_direction = direction
        last_index = t

        signal = {
            'symbol': symbol,
            'time': candle_time,
            'period': period,
            'direction': direction,
            'price': closes.iloc[t],
            'indicators': ', '.join(agreeing),
        }
        for h in EVAL_HORIZONS:
            change = price_change_percent(closes, t, h)
            if direction == Signal.SHORT:
                change = -change   # uno short guadagna quando il prezzo scende
            signal[f'result_{h}'] = change - EVAL_FEE_PERCENT
        signals.append(signal)
    return signals, candles


def print_report(signals, candles):
    print()
    print('=' * 100)
    print('RISULTATI DELLA VALUTAZIONE')
    print(f'Timeframe {TIMEFRAME}. Risultati in % al netto delle commissioni ({EVAL_FEE_PERCENT}% andata e ritorno).')
    print('"A caso" = entrare in una candela qualsiasi, nella stessa direzione e nello stesso periodo.')
    print('=' * 100)
    if len(signals) == 0:
        print('Nessun segnale trovato.')
        return

    for period in [1, 2]:
        period_candles = candles[candles['period'] == period]
        start = period_candles['time'].min().strftime('%Y-%m-%d')
        end = period_candles['time'].max().strftime('%Y-%m-%d')
        print()
        print(f'--- PERIODO {period} ({start} -> {end}) ---')
        for direction in [Signal.LONG, Signal.SHORT]:
            selected = signals[(signals['direction'] == direction) & (signals['period'] == period)]
            note = ''
            if 0 < len(selected) < MIN_RELIABLE_SIGNALS:
                note = '  (pochi segnali: risultato poco affidabile)'
            print(f'{direction}: {len(selected)} segnali{note}')
            if len(selected) == 0:
                continue
            for h in EVAL_HORIZONS:
                results = selected[f'result_{h}']
                random_results = period_candles[f'change_{h}']
                if direction == Signal.SHORT:
                    random_results = -random_results
                random_results = random_results - EVAL_FEE_PERCENT
                winners = (results > 0).mean() * 100
                random_winners = (random_results > 0).mean() * 100
                difference = results.mean() - random_results.mean()
                print(f'   dopo {h:>3} candele:  media {results.mean():+.2f}%  vincenti {winners:3.0f}%'
                      f'   |  a caso: media {random_results.mean():+.2f}%  vincenti {random_winners:3.0f}%'
                      f'   |  differenza {difference:+.2f}%')
    print()


def save_signals(signals):
    '''salva l'elenco di tutti i segnali in un file CSV, da aprire anche con Excel'''
    if len(signals) == 0:
        return
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    file_name = os.path.join(RESULTS_FOLDER, 'valutazione_' + time.strftime('%Y%m%d_%H%M') + '.csv')
    signals.to_csv(file_name, index=False)
    logger.info('Elenco dei segnali salvato in %s', file_name)
