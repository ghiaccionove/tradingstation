# Modello di configurazione.
# Copia questo file in config.py e inserisci i tuoi valori.
# config.py NON va mai caricato su git (è già in .gitignore).

# Chiavi API per ogni exchange (servono solo per inviare ordini,
# per leggere i dati di mercato si possono lasciare vuote)
API_KEYS = {
    'krakenfutures': {
        'api_key': '',
        'api_secret': ''
    },
    'kraken': {
        'api_key': '',
        'api_secret': ''
    }
}

# Bot Telegram per ricevere gli avvisi
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

# Nome dell'exchange da usare (nome ccxt).
# Su Kraken: 'krakenfutures' = perpetual/futures, 'kraken' = spot
EXCHANGE_NAME = 'krakenfutures'

# Tipo di mercato: 'swap' = perpetual, 'spot' = a pronti, 'future' = con scadenza
MARKET_TYPE = 'swap'
