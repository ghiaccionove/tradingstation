import talib
import numpy as np

def volatility(data, period=60):
    '''calcola la volatilità annualizzata degli utlimi n periodi'''
    data['returns'] = np.log(data['close'] / data['close'].shift(1))
    data[f'volatility{period}'] = data['returns'].rolling(period).std() * ((60) ** 0.5)
    return data

#valuta se ritornare intero dataframe o slo la serie dell'indicatore

def rsi(data, period=14):
    data['rsi'] = talib.RSI(data['close'], timeperiod=period)
    return data

def parabolic_sar(data, acceleration=0.02, maximum=0.2):
    data['sar'] = talib.SAR(data['high'], data['low'], acceleration=acceleration, maximum=maximum)
    return data

