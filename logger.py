import logging

logger = logging.getLogger('TradingStation')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('trading_station.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(module)s - %(funcName)s - Line %(lineno)d - %(levelname)s - %(message)s'
)
console_formatter = logging.Formatter(
    '%(name)s - %(levelname)s - %(message)s'
)

file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

# Aggiunta degli handler al logger principale
logger.addHandler(file_handler)
logger.addHandler(console_handler)
