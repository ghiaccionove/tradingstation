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

