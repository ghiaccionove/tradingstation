from modes.spotter_mode import spotter
from modes.manual_mode import manual
from modes.closing_mode import shutter
from modes.evaluate_mode import evaluate
from logger import logger
from utils.exchange_manager import Exchange
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from utils.data_fetcher import fetch_symbols
from utils import completers
from config import EXCHANGE_NAME
from settings import PROFILES

def ask_profile(session):
        '''chiede quale profilo usare (definiti in settings.py); None se il nome non esiste'''
        profile_name = session.prompt('Quale profilo? > ', completer=completers.profile_completer)
        if profile_name not in PROFILES:
                logger.info('Profilo "%s" non trovato. Profili disponibili: %s', profile_name, ', '.join(PROFILES))
                return None
        return profile_name

def main():
        session = PromptSession()
        logger.info('Avvio Trading Station...')
        exchange = Exchange(EXCHANGE_NAME) # il nome dell'exchange si sceglie in config.py

        mode_input = session.prompt('Trading Station Mode > ', completer=completers.mode_completer)
        if mode_input == 'spotter':
                profile_name = ask_profile(session)
                if profile_name is not None:
                        spotter(exchange,profile_name)
        elif mode_input == 'evaluate':
                profile_name = ask_profile(session)
                if profile_name is not None:
                        evaluate(exchange,profile_name)
        elif mode_input == 'shut':
                shutter(exchange)
        elif mode_input == 'auto':
                logger.info('WORK IN PROGRESS') #implement logic 
        elif mode_input == 'manual':
                logger.info('Starting manual trading session...')
                while True:                        
                        params = {}
                        extra_params = {}
                        params['ordertype'] = session.prompt('Che tipo di ordine vuoi effettuare? > ',completer=completers.order_completer)
                        if params['ordertype'] == 'exit':
                                break
                        params['symbol'] = session.prompt('Inserisci il simbolo su cui effettuare operazione > ', completer=completers.symbol_completer(exchange))
                        if params['ordertype'] != 'cancel':
                                params['side'] = session.prompt('buy or sell? > ', completer=[])
                                params['amount'] = float(session.prompt('Inserisci quantità > ', completer=[]))
                                if params['ordertype'] == 'limit':
                                        params['price'] = float(session.prompt('Inserisci prezzo > '))
                                extra_params['reduceOnly'] = session.prompt('Reduce only order? (y/n) > ').strip().lower() == 'y'

                        manual(exchange,params,extra_params)

if __name__ == '__main__':
        main()


