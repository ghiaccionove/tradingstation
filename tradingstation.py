import pandas as pd
import numpy as np
import talib

class Indicators:
    def __init__(self, dataframe):
        self.data = dataframe

    def volatility(self, period=60):
        '''calcola la volatilità degli ultimi n periodi'''
        self.data['returns'] = np.log(self.data['close'] / self.data['close'].shift(1))
        self.data[f'volatility{period}'] = self.data['returns'].rolling(period).std() * ((60) ** 0.5)

    def parabolic_sar(self, acceleration=0.02, maximum=0.2):
        '''calcola parabolic SAR'''
        self.data['sar'] = talib.SAR(self.data['high'], self.data['low'], acceleration=acceleration, maximum=maximum)
    
    def rsi(self, period=14):
        '''calcola RSI'''
        self.data['rsi'] = talib.RSI(self.data['close'], timeperiod=period)

