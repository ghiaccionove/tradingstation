from prompt_toolkit.completion import WordCompleter
from utils.data_fetcher import fetch_symbols
from settings import PROFILES

mode_completer = WordCompleter(['spotter','evaluate','manual','auto','shut'])
profile_completer = WordCompleter(list(PROFILES))
order_completer = WordCompleter(['market','limit','cancel', 'exit'])

def symbol_completer(exchange):
    return WordCompleter(fetch_symbols(exchange, category='all'), ignore_case=True)
