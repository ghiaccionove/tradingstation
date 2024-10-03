from signals import indicators
from signals.signal_types import Signal
import pandas as pd


def rsi_signal(data, overbought=70, oversold=30):
    data = indicators.rsi(data)
    latest_rsi = data['rsi'].iloc[-1]
    if latest_rsi > overbought:
        print('rsi ipercomprato: ', latest_rsi)
        return Signal.OVERBOUGHT

    elif latest_rsi < oversold:
        print('rsi ipervenduto: ', latest_rsi)
        return Signal.OVERSOLD
    else:
        print('rsi: ', latest_rsi)


def volatility_signal(data, period=60, threshold=0.013):
    data = indicators.volatility(data, period=period)
    volatility_column = f'volatility{period}'
    latest_volatility = data[volatility_column].iloc[-1]
    if latest_volatility > threshold:
        print('volatility is over the threshold: ', latest_volatility)
        return Signal.HIGH_VOLATILITY
    else:
        return Signal.LOW_VOLATILITY
    

def parabolic_trend(data):
    data = indicators.parabolic_sar(data)
    latest_sar = data['sar'].iloc[-1]
    if data['close'].iloc[-1] >=  latest_sar:
        print('Price is up parabolic SAR', latest_sar)
        return Signal.UP
    else:
        print('Price is down parabolic SAR', latest_sar)
        return Signal.DOWN

