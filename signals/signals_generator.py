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
    if latest_ratio > threshold:
        logger.debug('ATR relativo sopra la soglia: %s', latest_ratio)
        return Signal.HIGH_VOLATILITY, latest_ratio
    else:
        return Signal.LOW_VOLATILITY, latest_ratio


def rsi_trend_signal(data, period=14):
    '''RSI letto come trend: sopra 50 prevalgono i rialzi (UP), sotto 50 i ribassi (DOWN)'''
    latest_rsi = indicators.rsi(data, period=period).iloc[-1]
    logger.debug('RSI: %s --> trend', latest_rsi)
    if latest_rsi > 50:
        return Signal.UP
    if latest_rsi < 50:
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
