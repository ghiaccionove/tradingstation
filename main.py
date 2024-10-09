from logger import logger
from utils.exchange_manager import Exchange
from utils.data_fetcher import *
from signals.signals_generator import *
from strategies.base_strategy import Valubot


def main():
    try:
        logger.info("Inizializzo il programma")
        exchange = Exchange('bybit')
        logger.info("Cerco i mercati più scambiati di oggi")
        symbols = fetch_symbols(exchange)
        most_traded_symbols = filter_symbols_by_volume(exchange, symbols)
        logger.info('Avvio ricerca delle condizioni di mercato')
        while True:
            for symbol in most_traded_symbols:
                data = fetch_market_data(exchange, symbol)
                Valubot(data, exchange).generate_signal(symbol)
    except Exception as e:
        logger.exception('Errore')

if __name__ == '__main__':
    main()