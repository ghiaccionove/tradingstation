import argparse
from modes.spotter_mode import spotter
from modes.manual_mode import manual
from modes.closing_mode import shutter
from logger import logger
from utils.exchange_manager import Exchange


def main():
        logger.info('Inizializzo Exchange')
        exchange = Exchange('bybit')
        parser = argparse.ArgumentParser(description='Trading Station')
        #mode arguments
        parser.add_argument('--mode', choices=['spotter', 'manual', 'auto', 'shutter'], help='Scegli la modalità di esecuzione')
        #spotter arguments
        parser.add_argument('--fetch', choices=['all', 'volume'], default='all', help='Scegli su quali simboli prendere i dati')
        #manual arguments
        parser.add_argument('--ordertype', choices=['market', 'limit', 'cancel'], help='Scegli la tipologia di ordine' )
        parser.add_argument('--symbol', type=str, help='Inserisci il nome del simbolo es. --> BTC/USDT:USDT')
        parser.add_argument('--side', choices=['buy','sell'], help='Scegli la direzione')
        parser.add_argument('--amount', type=float, help='Inserisci il quantitativo')
        parser.add_argument('--price', type=float, help='Inserisci il prezzo')
        parser.add_argument('--params', choices=['reduce'], default=None, help='Inserisci parametri aggiuntivi')
        args = parser.parse_args()
        extra_params = {}
        if args.params == 'reduce':
                extra_params['reduceOnly'] = True
        if args.mode == 'spotter':
                spotter(exchange,args.fetch)
        elif args.mode == 'manual':
                manual(exchange, args, extra_params)
        elif args.mode == 'auto':
                logger.info('Automatic trading bot starting...')
        elif args.mode == 'shutter':
                shutter(exchange)

if __name__ == '__main__':
        main()


