from logger import logger
from orders.ordermanager import OrderManager

def manual(exchange, args, extra_params):
    logger.info('Starting manual session')
    order_manager = OrderManager(exchange)
    if args.ordertype == 'market':
        order = order_manager.place_market_order(args.symbol, args.side, args.amount, extra_params)
        logger.info(order)
    elif args.ordertype == 'limit':
        order = order_manager.place_limit_order(args.symbol, args.side, args.amount, args.price, extra_params)
        logger.info(order)
    elif args.ordertype == 'cancel':
        order_manager.cancel_all_open_orders(args.symbol)