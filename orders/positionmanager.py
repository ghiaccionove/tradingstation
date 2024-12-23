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
    
    def check_reduce_only_order(self, position):
        ### PROBLEMA DEL FUTURO QUELLO CHE POTREBBERO ESSERE RILEVATI ANCHE GLI STOP LOSS, RISOLVERE AGGIUNGENDO IL SIDE OPPOSTO ALLA POSIZIONE
        open_orders = self.order_manager.get_open_orders(position['symbol'])
        if not open_orders:
            return False
        else:
            for order in open_orders:
                if order['reduceOnly'] == True and order['amount'] == position['contracts']:
                    logger.info('Ordine take profit già presente e aggiornato')
                    return True
                else:
                    return False

    def percent_closing(self, long_profit_percent=1.0034, short_profit_percent=0.9966):
        try:
            positions = self.get_open_positions()
            while len(positions) >= 1:
                for position in positions:
                    if float(position['contracts']) != 0:
                        avg_price = float(position['entryPrice'])
                        logger.debug('Avg price : %s', avg_price)
                        logger.debug('Dettagli sulla posizione: %s', position)
                        if position['side'] == 'long':
                            take_profit_price = avg_price * long_profit_percent
                            reduce_only = self.check_reduce_only_order(position)
                            if reduce_only == False:
                                logger.debug('take profit price: %s', take_profit_price)
                                logger.info('Piazzo ordine di take profit per %s a %s', position['symbol'], take_profit_price)
                                self.order_manager.place_limit_order(position['symbol'], 'sell', float(position['contracts']), take_profit_price, 
                                                                 params = {'reduceOnly':True} )
                        else:
                            take_profit_price = avg_price * short_profit_percent
                            reduce_only = self.check_reduce_only_order(position)
                            if reduce_only == False:
                                logger.debug('take profit price: %s', take_profit_price)
                                logger.info('Piazzo ordine di take profit per %s a %s', position['symbol'], take_profit_price)
                                self.order_manager.place_limit_order(position['symbol'], 'buy', float(position['contracts']), take_profit_price, 
                                                                 params = {'reduceOnly':True} )
                positions = self.get_open_positions()
        except Exception as e:
            logger.exception('errore nella chiusura')


    