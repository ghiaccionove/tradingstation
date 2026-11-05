# Impostazioni di trading.
# A differenza di config.py (chiavi e segreti), questo file È salvato su git.

from watchlists import WATCHLIST_ITALIA, WATCHLIST_USA

# --- Spotter ---

# Timeframe, indicatori, mercati, pausa, avvisi ripetuti e mercati fermi
# si scelgono nei PROFILI, in fondo al file.

# Quante candele scaricare per ogni simbolo (Kraken Futures ne dà al massimo 1000)
CANDLES_LIMIT = 1000

# Volume minimo nelle ultime 24 ore (in dollari) per il filtro 'volume'
MIN_VOLUME = 1000000

# Volume minimo per i mercati tradizionali (azioni, indici, materie prime, valute).
# Su Kraken Futures hanno volumi molto più bassi delle crypto: con 1 milione
# passavano solo 4 xStocks e oro/argento/petrolio, nessuna azione 'Equities'.
MIN_VOLUME_TRADFI = 300000

# --- Valutazione dei segnali (modalità 'evaluate') ---

# Quante candele storiche scaricare per ogni simbolo (es. 3000 candele da 15m = circa 31 giorni)
EVAL_CANDLES = 3000

# Come esce ogni trade simulato. Ogni riga è una prova: vengono misurate tutte, così si confrontano.
#   'max_candles' -> uscita a tempo: dopo quante candele si esce comunque, alla chiusura (obbligatorio).
#                    Si contano candele: a 1h un giorno di borsa è circa 8 candele, una settimana circa 40
#                    (le crypto sono sempre aperte: 24 e 168).
#   'take_profit' -> uscita a percentuale: obiettivo di guadagno, in % dal prezzo di entrata. None = nessun obiettivo
#   'stop_loss'   -> perdita massima, in % dal prezzo di entrata. None = nessuno stop
#   'take_profit_atr', 'stop_loss_atr' -> gli stessi, ma in multipli dell'ATR in % della candela di entrata.
#                    Es. 1.5 con ATR 2% = 3% dal prezzo di entrata: si adattano da soli a ogni titolo e momento.
#                    Per ognuno dei due si sceglie percentuale fissa OPPURE ATR, l'altro resta None.
#   'rsi_exit'    -> uscita con indicatore: livello dell'RSI a cui si esce, alla chiusura della candela.
#                    Un LONG esce quando l'RSI sale fin lì, uno SHORT quando scende fin lì. None = nessuna uscita con RSI
EVAL_EXITS = {
    'giorno':                   {'max_candles': 8,  'take_profit': None, 'stop_loss': None, 'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': None},
    'giorno_obiettivo':         {'max_candles': 8,  'take_profit': 1.5,  'stop_loss': None, 'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': None},
    'giorno_obiettivo_stop':    {'max_candles': 8,  'take_profit': 1.5,  'stop_loss': 1.0,  'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': None},
    'giorno_atr':               {'max_candles': 8,  'take_profit': None, 'stop_loss': None, 'take_profit_atr': 3.0,  'stop_loss_atr': 1.5,  'rsi_exit': None},
    'settimana':                {'max_candles': 40, 'take_profit': None, 'stop_loss': None, 'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': None},
    'settimana_obiettivo':      {'max_candles': 40, 'take_profit': 1.5,  'stop_loss': None, 'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': None},
    'settimana_obiettivo_stop': {'max_candles': 40, 'take_profit': 1.5,  'stop_loss': 1.0,  'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': None},
    'settimana_atr':            {'max_candles': 40, 'take_profit': None, 'stop_loss': None, 'take_profit_atr': 3.0,  'stop_loss_atr': 1.5,  'rsi_exit': None},
    'settimana_rsi':            {'max_candles': 40, 'take_profit': None, 'stop_loss': None, 'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': 50},
    'settimana_rsi_stop':       {'max_candles': 40, 'take_profit': None, 'stop_loss': 1.0,  'take_profit_atr': None, 'stop_loss_atr': None, 'rsi_exit': 50},
    'settimana_rsi_stop_atr':   {'max_candles': 40, 'take_profit': None, 'stop_loss': None, 'take_profit_atr': None, 'stop_loss_atr': 1.5,  'rsi_exit': 50},
}

# Commissioni di andata e ritorno, in percentuale.
# Kraken Futures: 0.05% per ordine 'taker' (al mercato) -> 0.10% tra entrata e uscita
EVAL_FEE_PERCENT = 0.10

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
#
# Ogni gruppo di impostazioni ha un nome e si usa nei profili (sotto).
# Per provare una strategia diversa: copiare il dizionario, dargli un altro nome,
# cambiare i valori e usarlo nel profilo voluto.
INDICATORS_BASE = {
    'rsi':        {'enabled': True, 'mode': 'reversal', 'period': 14, 'overbought': 66, 'oversold': 34},
    'sar':        {'enabled': True, 'mode': 'direction', 'acceleration': 0.02, 'maximum': 0.2, 'flip_candles': 3},
    'volatility': {'enabled': True, 'period': 60, 'threshold': 0.013},
    'atr':        {'enabled': False, 'period': 14, 'average_period': 100, 'threshold': 1.5},
}

# Azioni: RSI + ATR relativo. La volatilità all'1,3% orario è da crypto: sulle azioni non scatta quasi mai.
INDICATORS_AZIONI = {
    'rsi':        {'enabled': True, 'mode': 'reversal', 'period': 14, 'overbought': 66, 'oversold': 34},
    'sar':        {'enabled': False, 'mode': 'direction', 'acceleration': 0.02, 'maximum': 0.2, 'flip_candles': 3},
    'volatility': {'enabled': False, 'period': 60, 'threshold': 0.013},
    'atr':        {'enabled': True, 'period': 14, 'average_period': 100, 'threshold': 1.5},
}

# --- Profili ---

# All'avvio di spotter ed evaluate si sceglie un profilo. Ogni profilo dice:
#   'source'      -> da dove arrivano i dati: 'kraken' (exchange in config.py) oppure 'yahoo' (azioni, ETF)
#   'category'    -> solo Kraken: quali mercati, 'crypto', 'tradfi' oppure 'all'
#   'filter'      -> solo Kraken: 'volume' = solo i simboli sopra MIN_VOLUME / MIN_VOLUME_TRADFI, 'all' = tutti
#   'symbols'     -> solo Yahoo: la lista dei titoli da controllare (vedi watchlists.py)
#   'timeframe'   -> durata di ogni candela.
#                    Valori possibili su Kraken: '1m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w'
#                    Valori possibili su Yahoo: '1m' (storico 7 giorni), '5m', '15m', '30m' (60 giorni),
#                    '1h' (2 anni), '1d'
#   'indicators'  -> quale gruppo di indicatori usare (vedi sopra)
#   'min_signals' -> quanti indicatori accesi devono essere d'accordo per far partire un avviso:
#                    'all' = tutti quelli accesi (es. 3 su 3), un numero, es. 2 = almeno 2 (es. 2 su 3)
#   'platform'    -> dove si opera dopo l'avviso (viene scritto nel messaggio)
#   'pause_seconds' -> secondi di attesa tra un giro di controllo e il successivo.
#                    Conviene adattarla al timeframe: con candele da 1h non serve controllare ogni minuto.
#   'alert_cooldown_minutes' -> avvisi ripetuti: lo stesso avviso (stesso simbolo, stessa direzione)
#                    non viene reinviato prima di questi minuti. Se la direzione cambia
#                    (es. da LONG a SHORT) l'avviso parte subito. 0 = avviso a ogni giro.
#   'activity_candles', 'min_active_candles' -> mercati fermi: un simbolo viene saltato se nelle
#                    ultime 'activity_candles' candele meno di 'min_active_candles' hanno avuto un
#                    movimento di prezzo (massimo diverso dal minimo). Su mercati con pochi scambi
#                    gli indicatori danno segnali senza senso. 'min_active_candles' = 0 per non saltare nulla.
#                    Attenzione: si contano candele, non minuti (con 1h, 60 candele = 60 ore).
# Per seguire più profili insieme: avviare il programma in più terminali.
PROFILES = {
    'crypto': {
        'source': 'kraken',
        'category': 'crypto',
        'filter': 'volume',
        'timeframe': '1m',
        'indicators': INDICATORS_BASE,
        'min_signals': 'all',
        'platform': 'Kraken',
        'pause_seconds': 60,
        'alert_cooldown_minutes': 60,
        'activity_candles': 60,
        'min_active_candles': 10,
    },
    'tradfi': {
        'source': 'kraken',
        'category': 'tradfi',
        'filter': 'volume',
        'timeframe': '1m',
        'indicators': INDICATORS_BASE,
        'min_signals': 'all',
        'platform': 'Kraken',
        'pause_seconds': 60,
        'alert_cooldown_minutes': 60,
        'activity_candles': 60,
        'min_active_candles': 10,
    },
    'all': {
        'source': 'kraken',
        'category': 'all',
        'filter': 'volume',
        'timeframe': '1m',
        'indicators': INDICATORS_BASE,
        'min_signals': 'all',
        'platform': 'Kraken',
        'pause_seconds': 60,
        'alert_cooldown_minutes': 60,
        'activity_candles': 60,
        'min_active_candles': 10,
    },
    # Azioni: le borse sono aperte poche ore al giorno (Milano 9-17:30, USA 15:30-22 ora italiana).
    # I dati di Milano arrivano con circa 15 minuti di ritardo.
    'azioni_italia': {
        'source': 'yahoo',
        'symbols': WATCHLIST_ITALIA,
        'timeframe': '1h',
        'indicators': INDICATORS_AZIONI,
        'min_signals': 'all',
        'platform': 'Trade Republic',
        'pause_seconds': 300,
        'alert_cooldown_minutes': 240,
        'activity_candles': 20,
        'min_active_candles': 10,
    },
    'azioni_usa': {
        'source': 'yahoo',
        'symbols': WATCHLIST_USA,
        'timeframe': '1h',
        'indicators': INDICATORS_AZIONI,
        'min_signals': 'all',
        'platform': 'Kraken / Trade Republic',
        'pause_seconds': 300,
        'alert_cooldown_minutes': 240,
        'activity_candles': 20,
        'min_active_candles': 10,
    },
}
