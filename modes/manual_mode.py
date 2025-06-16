from logger import logger
from orders.ordermanager import OrderManager

def manual(exchange, params, extra_params):
    logger.info('Starting manual session')
    order_manager = OrderManager(exchange)
    if params['ordertype'] == 'market':
        order = order_manager.place_market_order(params['symbol'], params['side'], params['amount'], extra_params)
        logger.info(order)
    elif params['ordertype'] == 'limit':
        order = order_manager.place_limit_order(params['symbol'], params['side'], params['amount'], params['price'], extra_params)
        logger.info(order)
    elif params['ordertype'] == 'cancel':
        order_manager.cancel_all_open_orders(params['symbol'])