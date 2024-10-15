from logger import logger

class OrderManager:
    def __init__(self, exchange):
        self.exchange = exchange

    def place_market_order(self, symbol, side, amount, params={}):
        try:
            price = None
            order = self.exchange.ccxt.create_market_order(symbol, side, amount, price, params)
            logger.info('Market order placed')
            return order
        except Exception as e:
            logger.exception('Errore durante il piazzamento')

    def place_limit_order(self, symbol, side, amount, price, params={}):
        try:
            order = self.exchange.ccxt.create_limit_order(symbol, side, amount, price, params)
            logger.info('Limit order placed')
            return order
        except Exception as e:
            logger.exception('Errore durante il piazzamento')