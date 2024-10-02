from signals import indicators
import pandas as pd


def rsi_signal(data, overbought=70, oversell=30):
    data = indicators.rsi(data)
    latest_rsi = data['rsi'].iloc[-1]
    signal_oversell = False
    signal_overbought = False
    if latest_rsi > overbought:
        print('rsi ipercomprato: ', latest_rsi)
        signal_overbought = True

    elif latest_rsi < oversell:
        print('rsi ipervenduto: ', latest_rsi)
        signal_oversell = True
    else:
        print('rsi: ', latest_rsi)
    return signal_overbought, signal_oversell
    

def volatility_signal(data, period=60, threshold=0.013):
    data = indicators.volatility(data, period=period)
    volatility_column = f'volatility{period}'
    latest_volatility = data[volatility_column].iloc[-1]
    if latest_volatility > threshold:
        print('volatility is over the threshold: ', latest_volatility)
        signal_breakout = True
    else:
        signal_breakout = False
    return signal_breakout

    
def parabolic_trend(data):
    data = indicators.parabolic_sar(data)
    latest_sar = data['sar'].iloc[-1]
    if data['close'].iloc[-1] >  latest_sar:
        print('Price is up parabolic SAR')
        signal_uptrend = True
    else:
        print('Price is down parabolic SAR')
        signal_uptrend = False
    return signal_uptrend
