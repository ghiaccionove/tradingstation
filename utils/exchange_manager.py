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
        self.ccxt.load_markets()
        if exchange_name == 'kraken':
            self.add_kraken_stocks()

    def add_kraken_stocks(self):
        '''
        aggiunge ai mercati le azioni tokenizzate di Kraken (xStocks, es. AAPLX/USD).
        ccxt non le carica da solo: vanno chieste a parte e unite agli altri mercati.
        '''
        stock_markets = self.ccxt.fetch_markets({'aclass_base': 'tokenized_asset'})
        all_markets = list(self.ccxt.markets.values()) + stock_markets
        self.ccxt.set_markets(all_markets, self.ccxt.currencies)

