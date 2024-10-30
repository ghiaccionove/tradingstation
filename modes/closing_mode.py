from logger import logger
from orders.positionmanager import PositionManager

def shutter(exchange):
    try:
        logger.info('Avvio Shutter Mode...')
        position_manager = PositionManager(exchange)
        position_manager.percent_closing()
        logger.info('Tutte le posizioni sono chiuse')
    except Exception as e:
        logger.exception('Errore nello shutter') 


