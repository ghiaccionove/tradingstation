'''
Modalità 'evaluate': valuta i segnali sui dati storici.

Scorre la storia candela per candela vedendo solo il passato, esattamente come farebbe
lo spotter dal vivo (stessi voti, stessa finestra di candele, stesso filtro sui mercati
fermi, stesso blocco degli avvisi ripetuti). Ogni segnale diventa un trade simulato, con
le uscite scelte in EVAL_EXITS (settings.py): a tempo, a percentuale, con o senza stop loss.
Il risultato si confronta con l'entrare "a caso" nella stessa direzione e con le stesse uscite.
'''
import os
import time
import pandas as pd
from logger import logger
from utils.data_fetcher import count_active_candles
from utils.sources import get_symbols, get_history
from signals.votes import get_votes, decide
from signals.signal_types import Signal
from signals.indicators import get_candle_minutes
from modes.spotter_mode import log_indicator_settings
from settings import PROFILES, CANDLES_LIMIT
from settings import EVAL_CANDLES, EVAL_EXITS, EVAL_FEE_PERCENT

# candele iniziali da non valutare: servono agli indicatori per "scaldarsi"
WARMUP_CANDLES = 200

# sotto questo numero di segnali il risultato è poco affidabile
MIN_RELIABLE_SIGNALS = 30

# cartella dove salvare l'elenco dei segnali (esclusa da git)
RESULTS_FOLDER = 'evaluations'


def evaluate(exchange, profile_name):
    try:
        profile = PROFILES[profile_name]
        logger.info('Profilo: %s', profile_name)
        symbols = get_symbols(exchange, profile)
        log_indicator_settings(profile)
        logger.info('Valutazione su %s candele da %s per simbolo', EVAL_CANDLES, profile['timeframe'])
        all_signals = []
        all_candles = []   # tutte le candele valutate, per il confronto "a caso"
        number = 0
        for symbol in symbols:
            number = number + 1
            logger.info('[%s/%s] %s', number, len(symbols), symbol)
            try:
                data = get_history(exchange, symbol, EVAL_CANDLES, profile)
                signals, candles = evaluate_symbol(data, symbol, profile)
                all_signals = all_signals + signals
                all_candles = all_candles + candles
            except Exception as e:
                logger.info('Errore su %s, lo salto: %s', symbol, e)
        signals_table = pd.DataFrame(all_signals)
        candles_table = pd.DataFrame(all_candles)
        print_report(signals_table, candles_table, profile['timeframe'])
        save_signals(signals_table)
    except KeyboardInterrupt:
        logger.info('Valutazione interrotta')


def get_longest_trade():
    '''la durata massima tra le uscite scelte, in candele'''
    longest = 0
    for exit_settings in EVAL_EXITS.values():
        longest = max(longest, exit_settings['max_candles'])
    return longest


def trade_percent(entry_price, price, direction):
    '''guadagno (o perdita, se negativo) in % di un trade, se uscisse a questo prezzo'''
    change = (price / entry_price - 1) * 100
    if direction == Signal.SHORT:
        change = -change   # uno short guadagna quando il prezzo scende
    return change


def simulate_trade(prices, t, direction, exit_settings):
    '''
    simula un trade entrato alla chiusura della candela t, guardando una alla volta le candele successive.
    Restituisce il risultato in % (al netto delle commissioni), il motivo dell'uscita
    ('stop', 'target' o 'time') e per quante candele il trade è rimasto aperto.
    '''
    entry_price = prices['close'][t]
    stop_loss = exit_settings['stop_loss']
    take_profit = exit_settings['take_profit']
    for candles_held in range(1, exit_settings['max_candles'] + 1):
        i = t + candles_held
        if direction == Signal.LONG:
            worst_price = prices['low'][i]
            best_price = prices['high'][i]
        else:
            worst_price = prices['high'][i]
            best_price = prices['low'][i]
        # lo stop si controlla per primo: se in una candela vengono toccati sia lo stop sia
        # l'obiettivo non sappiamo quale sia arrivato prima, e per prudenza contiamo la perdita
        if stop_loss is not None and trade_percent(entry_price, worst_price, direction) <= -stop_loss:
            # se il prezzo apre già oltre lo stop (es. salto durante la notte) si esce all'apertura, a un prezzo peggiore
            open_result = trade_percent(entry_price, prices['open'][i], direction)
            return min(-stop_loss, open_result) - EVAL_FEE_PERCENT, 'stop', candles_held
        if take_profit is not None and trade_percent(entry_price, best_price, direction) >= take_profit:
            return take_profit - EVAL_FEE_PERCENT, 'target', candles_held
    # né stop né obiettivo: si esce alla chiusura dell'ultima candela
    last_price = prices['close'][t + exit_settings['max_candles']]
    return trade_percent(entry_price, last_price, direction) - EVAL_FEE_PERCENT, 'time', exit_settings['max_candles']


def evaluate_symbol(data, symbol, profile):
    '''
    scorre la storia di un simbolo con la strategia del profilo e restituisce due elenchi:
    - signals: i segnali trovati, ognuno con il risultato di ogni uscita (al netto delle commissioni)
    - candles: tutte le candele valutate, con il risultato di un trade qualsiasi (serve per il confronto "a caso")
    '''
    signals = []
    candles = []
    longest_trade = get_longest_trade()
    if len(data) < WARMUP_CANDLES + longest_trade + 1:
        logger.info('%s: storico troppo corto, lo salto', symbol)
        return signals, candles

    closes = data['close']
    # liste semplici: i trade simulati leggono molti prezzi e così è molto più veloce
    prices = {
        'open': data['open'].tolist(),
        'high': data['high'].tolist(),
        'low': data['low'].tolist(),
        'close': closes.tolist(),
    }
    cooldown_candles = profile['alert_cooldown_minutes'] / get_candle_minutes(data)
    last_direction = None
    last_index = None
    # ci servono candele "future" per simulare i trade: ci fermiamo prima della fine
    last_t = len(data) - longest_trade
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
        if count_active_candles(window, profile['activity_candles']) < profile['min_active_candles']:
            continue   # mercato fermo: lo spotter lo salterebbe

        # ogni candela valutata serve al confronto "a caso"
        candle = {'time': candle_time, 'period': period}
        for name, exit_settings in EVAL_EXITS.items():
            for direction in [Signal.LONG, Signal.SHORT]:
                result, reason, candles_held = simulate_trade(prices, t, direction, exit_settings)
                candle[f'{name}_{direction}'] = result
        candles.append(candle)

        direction, agreeing, enabled_count = decide(get_votes(window, profile['indicators']), profile['min_signals'])
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
        for name, exit_settings in EVAL_EXITS.items():
            result, reason, candles_held = simulate_trade(prices, t, direction, exit_settings)
            signal[f'{name}_result'] = result
            signal[f'{name}_reason'] = reason
            signal[f'{name}_candles'] = candles_held
        signals.append(signal)
    return signals, candles


def print_report(signals, candles, timeframe):
    print()
    print('=' * 100)
    print('RISULTATI DELLA VALUTAZIONE')
    print(f'Timeframe {timeframe}. Risultati in % al netto delle commissioni ({EVAL_FEE_PERCENT}% andata e ritorno).')
    print('"A caso" = entrare in una candela qualsiasi, nella stessa direzione, nello stesso periodo e con le stesse uscite.')
    print('Uscite = quanti trade sono usciti su obiettivo / stop / a tempo. Candele = durata media del trade.')
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
            for name in EVAL_EXITS:
                print_exit_line(name, selected, period_candles[f'{name}_{direction}'])
    print()


def print_exit_line(name, selected, random_results):
    '''scrive la riga del report per una uscita: risultato dei segnali, come sono usciti e confronto "a caso"'''
    results = selected[f'{name}_result']
    reasons = selected[f'{name}_reason']
    target_percent = (reasons == 'target').mean() * 100
    stop_percent = (reasons == 'stop').mean() * 100
    time_percent = (reasons == 'time').mean() * 100
    winners = (results > 0).mean() * 100
    random_winners = (random_results > 0).mean() * 100
    difference = results.mean() - random_results.mean()
    print(f'   {name:<26} media {results.mean():+.2f}%  vincenti {winners:3.0f}%'
          f'  uscite {target_percent:3.0f}/{stop_percent:3.0f}/{time_percent:3.0f}%'
          f'  candele {selected[f"{name}_candles"].mean():4.1f}'
          f'  |  a caso: media {random_results.mean():+.2f}%  vincenti {random_winners:3.0f}%'
          f'  |  differenza {difference:+.2f}%')


def save_signals(signals):
    '''salva l'elenco di tutti i segnali in un file CSV, da aprire anche con Excel'''
    if len(signals) == 0:
        return
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    file_name = os.path.join(RESULTS_FOLDER, 'valutazione_' + time.strftime('%Y%m%d_%H%M') + '.csv')
    signals.to_csv(file_name, index=False)
    logger.info('Elenco dei segnali salvato in %s', file_name)
