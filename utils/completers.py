from prompt_toolkit.completion import WordCompleter
from utils.data_fetcher import fetch_symbols 

mode_completer = WordCompleter(['spotter','manual','auto','shut'])
fetch_completer = WordCompleter(['all','volume'])
order_completer = WordCompleter(['market','limit','cancel', 'exit'])

def symbol_completer(exchange):
    return WordCompleter(fetch_symbols(exchange), ignore_case=True)
