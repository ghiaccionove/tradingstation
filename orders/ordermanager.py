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
            #coin_amount = self.exchange.ccxt.amount_to_precision(symbol, amount/price) DA METTERE IN UN ALTRO MODO 
            order = self.exchange.ccxt.create_limit_order(symbol, side, amount, price, params)
            logger.info('Limit order placed')
            return order
        except Exception as e:
            logger.exception('Errore durante il piazzamento')

    def cancel_all_open_orders(self, symbol):
        try:
            self.exchange.ccxt.cancel_all_orders(symbol)
            logger.info('Order deleted')
        except Exception as e:
            logger.exception('Errore durante la cancellazione')

    def get_open_orders(self, symbol=None):
        try:
            logger.info('Recupero ordini aperti')
            open_orders = self.exchange.ccxt.fetch_open_orders(symbol)
            return open_orders
        except Exception as e:
            logger.exception('Errore nel recuperare ordini aperti')
    


