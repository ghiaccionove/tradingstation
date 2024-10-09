import logging
from alerts.telegram_handler import TelegramHandler

logger = logging.getLogger('TradingStation')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('trading_station.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(module)s - %(funcName)s - Line %(lineno)d - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    '%(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

telegram_handler = TelegramHandler()
telegram_handler.setLevel(logging.WARNING)
telegram_formatter = logging.Formatter(
    '%(message)s'
)
telegram_handler.setFormatter(telegram_formatter)
logger.addHandler(telegram_handler)