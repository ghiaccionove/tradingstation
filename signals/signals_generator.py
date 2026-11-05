from signals import indicators
from signals.signal_types import Signal
import pandas as pd
from logger import logger

def rsi_signal(data, overbought=70, oversold=30, period=14):
    latest_rsi = indicators.rsi(data, period=period).iloc[-1]
    if latest_rsi > overbought:
        logger.debug('RSI: %s --> ipercomprato', latest_rsi)
        return Signal.OVERBOUGHT

    elif latest_rsi < oversold:
        logger.debug('RSI: %s --> ipervenduto', latest_rsi)
        return Signal.OVERSOLD
    else:
        logger.debug('RSI: %s --> neutro', latest_rsi)


def volatility_signal(data, period=60, threshold=0.013):
    latest_volatility = indicators.volatility(data, period=period).iloc[-1]
    if latest_volatility > threshold:
        logger.debug('volatility is over the threshold: %s', latest_volatility)
        return Signal.HIGH_VOLATILITY, latest_volatility
    else:
        return Signal.LOW_VOLATILITY, latest_volatility
    

def parabolic_trend(data, acceleration=0.02, maximum=0.2):
    latest_sar = indicators.parabolic_sar(data, acceleration=acceleration, maximum=maximum).iloc[-1]
    if data['close'].iloc[-1] >=  latest_sar:
        logger.debug('Price is up parabolic SAR: %s', latest_sar)
        return Signal.UP
    else:
        logger.debug('Price is down parabolic SAR: %s', latest_sar)
        return Signal.DOWN


def atr_signal(data, period=14, average_period=100, threshold=1.5):
    latest_ratio = indicators.atr_ratio(data, period=period, average_period=average_period).iloc[-1]
    logger.debug('ATR relativo: %s (soglia %s)', latest_ratio, threshold)
    if latest_ratio > threshold:
        return Signal.HIGH_VOLATILITY, latest_ratio
    else:
        return Signal.LOW_VOLATILITY, latest_ratio


def atr_percent_signal(data, period=14, threshold=0.5):
    latest_atr_percent = indicators.atr_percent(data, period=period).iloc[-1]
    logger.debug('ATR in percentuale: %s (soglia %s)', latest_atr_percent, threshold)
    if latest_atr_percent > threshold:
        return Signal.HIGH_VOLATILITY, latest_atr_percent
    else:
        return Signal.LOW_VOLATILITY, latest_atr_percent


def compare_values(first, second):
    '''UP se il primo valore è più alto, DOWN se è più basso, None se sono uguali o manca un dato'''
    if first > second:
        return Signal.UP
    if first < second:
        return Signal.DOWN
    return None


def read_cross(line, average):
    '''UP se la linea ha appena incrociato la sua media verso l'alto, DOWN verso il basso, altrimenti None'''
    if line.iloc[-2] <= average.iloc[-2] and line.iloc[-1] > average.iloc[-1]:
        return Signal.UP
    if line.iloc[-2] >= average.iloc[-2] and line.iloc[-1] < average.iloc[-1]:
        return Signal.DOWN
    return None


def read_line(line, mode, ma_type, ma_period):
    '''
    lettura comune a tutte le linee (RSI, volume, ...). Restituisce UP, DOWN o None:
    'rising'    -> la linea sale o scende rispetto alla candela prima
    'ma_rising' -> la sua media mobile sale o scende rispetto alla candela prima
    'above'     -> la linea è sopra o sotto la sua media mobile
    'cross'     -> la linea ha appena incrociato la sua media mobile
    '''
    if mode == 'rising':
        return compare_values(line.iloc[-1], line.iloc[-2])
    average = indicators.moving_average(line, ma_period, ma_type)
    if mode == 'ma_rising':
        return compare_values(average.iloc[-1], average.iloc[-2])
    if mode == 'above':
        return compare_values(line.iloc[-1], average.iloc[-1])
    if mode == 'cross':
        return read_cross(line, average)
    raise ValueError(f"mode '{mode}' non valido: usare 'rising', 'ma_rising', 'above' o 'cross'")


def rsi_line_signal(data, mode, ma_type, ma_period, period=14, oversold=None, overbought=None):
    '''
    RSI letto insieme alla sua media mobile (vedi read_line). Livelli facoltativi: con `oversold`
    il segnale UP vale solo se l'RSI è ancora sotto quel livello, con `overbought` il DOWN solo se è sopra.
    '''
    line = indicators.rsi(data, period=period)
    signal = read_line(line, mode, ma_type, ma_period)
    logger.debug('RSI: %s, lettura %s --> %s', line.iloc[-1], mode, signal)
    if signal == Signal.UP and oversold is not None and line.iloc[-1] >= oversold:
        return None
    if signal == Signal.DOWN and overbought is not None and line.iloc[-1] <= overbought:
        return None
    return signal


def volume_line_signal(data, mode, ma_type, ma_period):
    '''volume letto insieme alla sua media mobile (vedi read_line)'''
    signal = read_line(indicators.volume_line(data), mode, ma_type, ma_period)
    logger.debug('Volume: %s, lettura %s --> %s', data['volume'].iloc[-1], mode, signal)
    return signal


def volume_spike_signal(data, days=20, threshold=2.0):
    '''volume anomalo nell'ultima candela: HIGH_VOLUME, altrimenti None'''
    latest_ratio = indicators.volume_ratio(data, days=days).iloc[-1]
    logger.debug('Volume relativo: %s (soglia %s)', latest_ratio, threshold)
    if latest_ratio > threshold:
        return Signal.HIGH_VOLUME
    return None


def volume_climax_signal(data, days=20, threshold=2.0, recent_candles=3):
    '''
    climax: una candela con volume anomalo nelle ultime `recent_candles`.
    Restituisce la direzione di quella candela (la più recente, se sono più di una):
    DOWN se ha chiuso in calo, UP se ha chiuso in salita, None se nessuna.
    '''
    ratios = indicators.volume_ratio(data, days=days)
    for candles_back in range(1, recent_candles + 1):
        if ratios.iloc[-candles_back] > threshold:
            logger.debug('Volume anomalo %s candele fa: %s', candles_back, ratios.iloc[-candles_back])
            if data['close'].iloc[-candles_back] < data['open'].iloc[-candles_back]:
                return Signal.DOWN
            if data['close'].iloc[-candles_back] > data['open'].iloc[-candles_back]:
                return Signal.UP
            return None
    return None


def rsi_trend_signal(data, period=14, trend_long=50, trend_short=50):
    '''
    RSI letto come trend: sopra `trend_long` prevalgono i rialzi (UP), sotto `trend_short` i ribassi (DOWN).
    Tra i due livelli il trend non è chiaro: nessun segnale.
    '''
    # con i livelli invertiti un RSI tra i due sarebbe insieme rialzo e ribasso
    if trend_long < trend_short:
        raise ValueError(f"trend_long ({trend_long}) non può essere sotto trend_short ({trend_short})")
    latest_rsi = indicators.rsi(data, period=period).iloc[-1]
    logger.debug('RSI: %s --> trend (long sopra %s, short sotto %s)', latest_rsi, trend_long, trend_short)
    if latest_rsi > trend_long:
        return Signal.UP
    if latest_rsi < trend_short:
        return Signal.DOWN
    return None


def parabolic_flip(data, acceleration=0.02, maximum=0.2, flip_candles=3):
    '''
    SAR letto come inversione: restituisce UP o DOWN solo se il SAR si è "girato"
    (il prezzo lo ha attraversato) nelle ultime `flip_candles` candele, altrimenti None.
    '''
    sar = indicators.parabolic_sar(data, acceleration=acceleration, maximum=maximum)
    price_above = data['close'] >= sar          # True = prezzo sopra il SAR, per ogni candela
    now_above = price_above.iloc[-1]
    previous = price_above.iloc[-flip_candles - 1:-1]   # le candele precedenti all'ultima
    # se almeno una delle candele precedenti era dall'altra parte, il giro è recente
    if (previous != now_above).any():
        if now_above:
            logger.debug('SAR girato al rialzo da poco')
            return Signal.UP
        logger.debug('SAR girato al ribasso da poco')
        return Signal.DOWN
    return None
