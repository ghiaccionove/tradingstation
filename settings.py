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

# --- Indicatori ---

# Ogni indicatore si accende/spegne con 'enabled' e ha i suoi parametri.
# Ogni indicatore acceso "vota" una direzione:
#   rsi        -> LONG se ipervenduto (sotto 'oversold'), SHORT se ipercomprato (sopra 'overbought')
#   sar        -> LONG se il prezzo è sopra il SAR parabolico, SHORT se è sotto
#   volatility -> se la volatilità supera 'threshold' conferma entrambe le direzioni (BOTH)
INDICATORS = {
    'rsi':        {'enabled': True, 'period': 14, 'overbought': 66, 'oversold': 34},
    'sar':        {'enabled': True, 'acceleration': 0.02, 'maximum': 0.2},
    'volatility': {'enabled': True, 'period': 60, 'threshold': 0.013},
}

# Quanti indicatori accesi devono essere d'accordo per far partire un avviso.
#   'all' -> tutti quelli accesi (es. 3 su 3)
#   un numero, es. 2 -> almeno 2 di quelli accesi (es. 2 su 3)
MIN_SIGNALS = 'all'
