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
