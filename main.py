import argparse
from modes.spotter_mode import spotter
from logger import logger
from utils.exchange_manager import Exchange


def main():
        logger.info('Inizializzo Exchange')
        exchange = Exchange('bybit')
        parser = argparse.ArgumentParser(description='Trading Station')
        parser.add_argument('--mode', choices=['spotter', 'manual', 'auto'], help='Scegli la modalità di esecuzione')
        parser.add_argument('--fetch', choices=['all', 'volume'], default='all', help='Scegli su quali simboli prendere i dati')
        args = parser.parse_args()
        if args.mode == 'spotter':
                spotter(exchange,args.fetch)
        elif args.mode == 'manual':
                logger.info('Manual trading session...')
        elif args.mode == 'auto':
                logger.info('Automatic trading bot starting...')

if __name__ == '__main__':
        main()


