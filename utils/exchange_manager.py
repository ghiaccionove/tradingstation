import ccxt
from config import API_KEYS

class Exchange:
    '''inizializzazione dell'istanza dell'exchange'''
    def __init__(self, exchange_name):
        exchange_class = getattr(ccxt, exchange_name)
        self.ccxt = exchange_class({
            'apiKey': API_KEYS[exchange_name]['api_key'],
            'secret': API_KEYS[exchange_name]['api_secret'],
            'enableRateLimit': True
        })


