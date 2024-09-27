from signals import indicators
import pandas as pd


def rsi_signal(data, overbought=70, oversell=30):
    data = indicators.rsi(data)
    latest_rsi = data['rsi'].iloc[-1]
    if latest_rsi > overbought:
        print('rsi ipercomprato: ', latest_rsi)
    elif latest_rsi < oversell:
        print('rsi ipervenduto: ', latest_rsi)
    else:
        print('rsi: ', latest_rsi)
    #return latest_rsi
    

def volatility_signal(data, period=60, threshold=0.013):
    data = indicators.volatility(data, period=period)
    volatility_column = f'volatility{period}'
    latest_volatility = data[volatility_column].iloc[-1]
    if latest_volatility > threshold:
        print('volatility is over the threshold: ', latest_volatility)
    else:
        print('volatility: ', latest_volatility)

    