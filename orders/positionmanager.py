from logger import logger
from orders.ordermanager import OrderManager

class PositionManager:
    def __init__(self, exchange):
        self.exchange = exchange
        self.order_manager = OrderManager(exchange)

    def get_open_positions(self):
        logger.info('Recupero le posizioni aperte...')
        positions = self.exchange.ccxt.fetch_positions()
        return positions
    
    def percent_closing(self, long_profit_percent=1.0034, short_profit_percent=0.9966):
        try:
            positions = self.get_open_positions()
            while len(positions) >= 1:
                for position in positions:
                    #chiedi se ci sono ordini 
                    if float(position['contracts']) != 0:
                        avg_price = float(position['entryPrice'])
                        logger.debug('Avg price : %s', avg_price)
                        logger.debug('Dettagli sulla posizione: %s', position)
                        if position['side'] == 'long':
                            take_profit_price = avg_price * long_profit_percent
                            logger.debug('take profit price: %s', take_profit_price)
                            logger.info('Piazzo ordine di take profit per %s a %s', position['symbol'], take_profit_price)
                            self.order_manager.place_limit_order(position['symbol'], 'sell', float(position['contracts']), take_profit_price, 
                                                                 params = {'reduceOnly':True} )
                        else:
                            take_profit_price = avg_price * short_profit_percent
                            logger.debug('take profit price: %s', take_profit_price)
                            logger.info('Piazzo ordine di take profit per %s a %s', position['symbol'], take_profit_price)
                            self.order_manager.place_limit_order(position['symbol'], 'buy', float(position['contracts']), take_profit_price, 
                                                                 params = {'reduceOnly':True} )
                positions = self.get_open_positions()
        except Exception as e:
            logger.exception('errore nella chiusura')


    