class BaseStrategy:
    def __init__(self, data, exchange):
        self.data = data
        self.exchange = exchange

    def generate_signal(self):
        raise NotImplementedError("Deve essere implementato dalla sottoclasse.")

from signals.signals_generator import *

class Valubot(BaseStrategy):
    def __init__(self, data, exchange, overbought=66, oversold=34, threshold=0.013):
        super().__init__(data, exchange)
        self.overbought = overbought
        self.oversold = oversold
        self.threshlod = threshold
    
    
    def generate_signal(self, symbol):
        rsi = rsi_signal(self.data, overbought=self.overbought, oversold=self.oversold)
        sar = parabolic_trend(self.data)
        volatility = volatility_signal(self.data, threshold=self.threshlod)

        if rsi == Signal.OVERSOLD and volatility == Signal.HIGH_VOLATILITY and sar == Signal.UP:
            logger.info('Long conditions for Valubot Strategy')
            logger.warning('Long conditions for Valubot Strategy in %s', symbol)
            return Signal.BUY
        elif rsi == Signal.OVERBOUGHT and volatility == Signal.HIGH_VOLATILITY and sar == Signal.DOWN:
            logger.info('Short conditions for Valubot Strategy')
            logger.warning('Short conditions for Valubot Strategy in %s', symbol)
            return Signal.SELL
        else:
            return 'Wait'
