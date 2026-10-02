# Impostazioni di trading.
# A differenza di config.py (chiavi e segreti), questo file È salvato su git.

# --- Spotter ---

# Durata di ogni candela.
# Valori possibili su Kraken: '1m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w'
TIMEFRAME = '1m'

# Quante candele scaricare per ogni simbolo (Kraken Futures ne dà al massimo 1000)
CANDLES_LIMIT = 1000

# Secondi di attesa tra un giro di controllo e il successivo
PAUSE_SECONDS = 60

# Volume minimo nelle ultime 24 ore (in dollari) per il filtro 'volume'
MIN_VOLUME = 1000000

# Mercati fermi: un simbolo viene saltato se nelle ultime ACTIVITY_CANDLES candele
# meno di MIN_ACTIVE_CANDLES hanno avuto un movimento di prezzo (massimo diverso dal minimo).
# Su mercati con pochi scambi gli indicatori danno segnali senza senso.
# Mettere MIN_ACTIVE_CANDLES = 0 per non saltare mai nulla.
ACTIVITY_CANDLES = 60
MIN_ACTIVE_CANDLES = 10

# Avvisi ripetuti: lo stesso avviso (stesso simbolo, stessa direzione) non viene
# reinviato prima che siano passati ALERT_COOLDOWN_MINUTES minuti.
# Se la direzione cambia (es. da LONG a SHORT) l'avviso parte subito.
# Mettere 0 per ricevere l'avviso a ogni giro.
ALERT_COOLDOWN_MINUTES = 60

# --- Indicatori ---

# Ogni indicatore si accende/spegne con 'enabled' e ha i suoi parametri.
# Alcuni indicatori hanno più modi di votare, scelti con 'mode'.
# Ogni indicatore acceso "vota" una direzione:
#   rsi        -> mode 'reversal' (inversione): LONG se ipervenduto (sotto 'oversold'),
#                                               SHORT se ipercomprato (sopra 'overbought')
#                 mode 'trend': LONG se RSI sopra 50, SHORT se sotto 50
#                               ('overbought' e 'oversold' non vengono usati)
#   sar        -> mode 'direction': vota sempre, LONG se il prezzo è sopra il SAR, SHORT se è sotto
#                 mode 'flip' (inversione): vota solo se il SAR si è girato nelle ultime
#                               'flip_candles' candele (LONG se girato al rialzo, SHORT se al ribasso)
#   volatility -> se la volatilità supera 'threshold' conferma entrambe le direzioni (BOTH)
#                 volatilità = movimento tipico del prezzo in un'ora, calcolato sulle ultime
#                 'period' candele (0.013 = 1,3% all'ora; mediana dei perpetual più scambiati ~0.008)
#   atr        -> ATR relativo: volatilità di adesso divisa per quella normale del simbolo.
#                 Se supera 'threshold' conferma entrambe le direzioni (BOTH).
#                 1.0 = normale, 1.5 = il 50% più agitato del solito (succede ~10% delle volte).
#                 'period' = candele per l'ATR, 'average_period' = candele per la media "normale".
#                 È un'alternativa a 'volatility': di solito se ne accende solo uno dei due.
INDICATORS = {
    'rsi':        {'enabled': True, 'mode': 'reversal', 'period': 14, 'overbought': 66, 'oversold': 34},
    'sar':        {'enabled': True, 'mode': 'direction', 'acceleration': 0.02, 'maximum': 0.2, 'flip_candles': 3},
    'volatility': {'enabled': True, 'period': 60, 'threshold': 0.013},
    'atr':        {'enabled': False, 'period': 14, 'average_period': 100, 'threshold': 1.5},
}

# Quanti indicatori accesi devono essere d'accordo per far partire un avviso.
#   'all' -> tutti quelli accesi (es. 3 su 3)
#   un numero, es. 2 -> almeno 2 di quelli accesi (es. 2 su 3)
MIN_SIGNALS = 2
