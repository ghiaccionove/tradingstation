import argparse
from modes.spotter_mode import spotter
from modes.manual_mode import manual
from modes.closing_mode import shutter
from logger import logger
from utils.exchange_manager import Exchange
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


def main():
        session = PromptSession()
        logger.info('Avvio Trading Station...')
        exchange = Exchange('bybit') #insert name of the exchange // don't know if others than bybit works lol
        #parser = argparse.ArgumentParser(description='Trading Station')

        mode_completer = WordCompleter(['spotter','manual','auto','shut'])
        fetch_completer = WordCompleter(['all','volume'])
        order_completer = WordCompleter(['market','limit','cancel'])

        mode_input = session.prompt('Trading Station Mode > ', completer=mode_completer)
        if mode_input == 'spotter':
                fetch_mode = session.prompt('Su quali simboli avvio la ricerca? > ', completer=fetch_completer)
                spotter(exchange,fetch_mode)
        elif mode_input == 'shut':
                shutter(exchange)
        elif mode_input == 'auto':
                logger.info('WORK IN PROGRESS') #implement logic 
        elif mode_input == 'manual':
                logger.info('Starting manual trading session...')
                params = {}
                extra_params = {}
                params['ordertype'] = session.prompt('Che tipo di ordine vuoi effettuare? > ',completer=order_completer)
                params['symbol'] = session.prompt('Inserisci il simbolo su cui effettuare operazione > ')
                if params['ordertype'] != 'cancel':
                        params['side'] = session.prompt('buy or sell? > ')
                        params['amount'] = float(session.prompt('Inserisci quantità da acquistare > '))
                        if params['ordertype'] == 'limit':
                                params['price'] = float(session.prompt('Inserisci prezzo > '))
                        extra_params['reduceOnly'] = session.prompt('Reduce only order? (y/n) > ').strip().lower() == 'y'

                manual(exchange,params,extra_params)

if __name__ == '__main__':
        main()


