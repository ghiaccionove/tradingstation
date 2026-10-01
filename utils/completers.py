from prompt_toolkit.completion import WordCompleter
from utils.data_fetcher import fetch_symbols 

mode_completer = WordCompleter(['spotter','manual','auto','shut'])
fetch_completer = WordCompleter(['all','volume'])
category_completer = WordCompleter(['crypto','tradfi','all'])
order_completer = WordCompleter(['market','limit','cancel', 'exit'])

def symbol_completer(exchange):
    return WordCompleter(fetch_symbols(exchange, category='all'), ignore_case=True)
