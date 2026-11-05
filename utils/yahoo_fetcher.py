'''
Candele da Yahoo Finance (libreria yfinance): azioni, ETF e indici di tutte le borse,
es. 'ENI.MI' (Milano), 'SAP.DE' (Xetra), 'AAPL' (USA).

Le funzioni restituiscono lo stesso DataFrame di ccxt
(timestamp in millisecondi, open, high, low, close, volume),
così indicatori, voti e valutazione funzionano senza modifiche.

Attenzione: Yahoo non è un servizio ufficiale per i programmi. Va bene per gli avvisi,
ma può cambiare o rifiutare le richieste se sono troppe.
I dati di Milano arrivano con circa 15 minuti di ritardo.
'''
import yfinance as yf
from logger import logger

# Quanto storico chiedere a Yahoo per ogni timeframe: è il massimo che Yahoo concede.
# Oltre questi limiti Yahoo non restituisce nessuna candela.
YAHOO_PERIODS = {
    '1m': '7d',
    '5m': '60d',
    '15m': '60d',
    '30m': '60d',
    '1h': '730d',
    '1d': 'max',
}

def download_yahoo(symbol, timeframe):
    '''scarica da Yahoo tutto lo storico disponibile per quel timeframe, nel formato di ccxt'''
    if timeframe not in YAHOO_PERIODS:
        raise ValueError(f"timeframe '{timeframe}' non disponibile su Yahoo: usare uno tra {list(YAHOO_PERIODS)}")
    raw = yf.Ticker(symbol).history(period=YAHOO_PERIODS[timeframe], interval=timeframe)
    # gli orari di Yahoo hanno il fuso orario della borsa (es. Europe/Rome):
    # li portiamo in UTC e in millisecondi, come quelli di ccxt
    timestamps = raw.index.tz_convert('UTC').astype('int64') // 1000000
    data = raw[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data.columns = ['open', 'high', 'low', 'close', 'volume']
    data.insert(0, 'timestamp', timestamps)
    data = data.dropna().reset_index(drop=True)
    # Yahoo dà prezzi con piccoli errori di arrotondamento (es. 349.29998779296875):
    # 4 decimali bastano anche per i titoli che valgono meno di un euro
    data[['open', 'high', 'low', 'close']] = data[['open', 'high', 'low', 'close']].round(4)
    return data

def fetch_yahoo_data(symbol, timeframe, limit):
    '''ultime `limit` candele, come fetch_market_data (l'ultima può essere ancora in corso)'''
    logger.info('%s', symbol)
    data = download_yahoo(symbol, timeframe)
    return data.tail(limit).reset_index(drop=True)

def fetch_yahoo_history(symbol, total_candles, timeframe):
    '''
    ultime `total_candles` candele chiuse, come fetch_history.
    Lo storico è limitato da Yahoo (vedi YAHOO_PERIODS): se ne servono di più, arrivano quelle disponibili.
    '''
    data = download_yahoo(symbol, timeframe)
    # l'ultima candela può essere ancora in corso: la togliamo, si valutano solo candele chiuse
    data = data.iloc[:-1]
    return data.tail(total_candles).reset_index(drop=True)
