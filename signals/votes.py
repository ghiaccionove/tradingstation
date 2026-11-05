'''
Votazione degli indicatori.

Ogni indicatore acceso nel profilo scelto (settings.py) "vota" una direzione:
LONG, SHORT, BOTH (conferma entrambe) oppure None (nessun segnale).
Poi si contano i voti: se abbastanza indicatori sono d'accordo, c'è un segnale.
'''
from signals.signal_types import Signal
from signals.signals_generator import rsi_signal, rsi_trend_signal, parabolic_trend, parabolic_flip
from signals.signals_generator import volatility_signal, atr_signal, atr_percent_signal
from signals.signals_generator import volume_spike_signal, volume_climax_signal
from signals.signals_generator import rsi_line_signal, volume_line_signal

# modi che leggono una linea insieme alla sua media mobile (vedi read_line in signals_generator.py)
LINE_MODES = ['rising', 'ma_rising', 'above', 'cross']


# --- Il voto di ogni indicatore ---

def rsi_vote(data, settings):
    mode = settings['mode']
    if mode == 'reversal':
        # inversione: è sceso troppo -> può rimbalzare (LONG), è salito troppo -> può scendere (SHORT)
        signal = rsi_signal(data, overbought=settings['overbought'], oversold=settings['oversold'],
                            period=settings['period'])
        if signal == Signal.OVERSOLD:
            return Signal.LONG
        if signal == Signal.OVERBOUGHT:
            return Signal.SHORT
        return None
    if mode == 'trend':
        # trend: sopra 'trend_long' prevalgono i rialzi (LONG), sotto 'trend_short' i ribassi (SHORT)
        signal = rsi_trend_signal(data, period=settings['period'], trend_long=settings['trend_long'],
                                  trend_short=settings['trend_short'])
        if signal == Signal.UP:
            return Signal.LONG
        if signal == Signal.DOWN:
            return Signal.SHORT
        return None
    if mode in LINE_MODES:
        # l'RSI insieme alla sua media mobile: sale o incrocia verso l'alto -> LONG, il contrario -> SHORT
        signal = rsi_line_signal(data, mode, settings['ma_type'], settings['ma_period'], period=settings['period'],
                                 oversold=settings['oversold'], overbought=settings['overbought'])
        if signal == Signal.UP:
            return Signal.LONG
        if signal == Signal.DOWN:
            return Signal.SHORT
        return None
    raise ValueError(f"mode '{mode}' non valido per rsi: usare 'reversal', 'trend' o uno tra {LINE_MODES}")

def sar_vote(data, settings):
    mode = settings['mode']
    if mode == 'direction':
        # vota sempre: prezzo sopra il SAR -> LONG, sotto -> SHORT
        signal = parabolic_trend(data, acceleration=settings['acceleration'], maximum=settings['maximum'])
        if signal == Signal.UP:
            return Signal.LONG
        return Signal.SHORT
    if mode == 'flip':
        # vota solo se il SAR si è girato da poco (nelle ultime 'flip_candles' candele)
        signal = parabolic_flip(data, acceleration=settings['acceleration'], maximum=settings['maximum'],
                                flip_candles=settings['flip_candles'])
        if signal == Signal.UP:
            return Signal.LONG
        if signal == Signal.DOWN:
            return Signal.SHORT
        return None
    raise ValueError(f"mode '{mode}' non valido per sar: usare 'direction' o 'flip'")

def volatility_vote(data, settings):
    signal, latest_volatility = volatility_signal(data, period=settings['period'],
                                                  threshold=settings['threshold'])
    if signal == Signal.HIGH_VOLATILITY:
        return Signal.BOTH
    return None

def atr_vote(data, settings):
    signal, latest_ratio = atr_signal(data, period=settings['period'],
                                      average_period=settings['average_period'],
                                      threshold=settings['threshold'])
    if signal == Signal.HIGH_VOLATILITY:
        return Signal.BOTH
    return None

def atr_percent_vote(data, settings):
    signal, latest_atr_percent = atr_percent_signal(data, period=settings['period'],
                                                    threshold=settings['threshold'])
    if signal == Signal.HIGH_VOLATILITY:
        return Signal.BOTH
    return None

def volume_vote(data, settings):
    mode = settings['mode']
    if mode == 'spike':
        # filtro: volume anomalo adesso, conferma entrambe le direzioni
        signal = volume_spike_signal(data, days=settings['days'], threshold=settings['threshold'])
        if signal == Signal.HIGH_VOLUME:
            return Signal.BOTH
        return None
    if mode == 'climax':
        # esaurimento: crollo con volume enorme -> i venditori possono aver finito (LONG), e viceversa
        signal = volume_climax_signal(data, days=settings['days'], threshold=settings['threshold'],
                                      recent_candles=settings['recent_candles'])
        if signal == Signal.DOWN:
            return Signal.LONG
        if signal == Signal.UP:
            return Signal.SHORT
        return None
    if mode in LINE_MODES:
        # il volume non dice da che parte andare: se fa ciò che chiede 'direction' conferma entrambe le direzioni
        signal = volume_line_signal(data, mode, settings['ma_type'], settings['ma_period'])
        if settings['direction'] == 'up':
            wanted = Signal.UP
        elif settings['direction'] == 'down':
            wanted = Signal.DOWN
        else:
            raise ValueError(f"direction '{settings['direction']}' non valida per volume: usare 'up' o 'down'")
        if signal == wanted:
            return Signal.BOTH
        return None
    raise ValueError(f"mode '{mode}' non valido per volume: usare 'spike', 'climax' o uno tra {LINE_MODES}")


# --- Raccolta e conteggio dei voti ---

def get_votes(data, indicators):
    '''
    calcola solo gli indicatori accesi e restituisce i loro voti, es.
    {'rsi': 'LONG', 'sar': 'LONG', 'volatility': None}
    indicators: le impostazioni degli indicatori del profilo (es. INDICATORS_BASE in settings.py)
    Per aggiungere un indicatore: scrivere la sua funzione ..._vote e aggiungere un blocco qui.
    '''
    votes = {}
    if indicators['rsi']['enabled']:
        votes['rsi'] = rsi_vote(data, indicators['rsi'])
    if indicators['sar']['enabled']:
        votes['sar'] = sar_vote(data, indicators['sar'])
    if indicators['volatility']['enabled']:
        votes['volatility'] = volatility_vote(data, indicators['volatility'])
    if indicators['atr']['enabled']:
        votes['atr'] = atr_vote(data, indicators['atr'])
    if indicators['atr_percent']['enabled']:
        votes['atr_percent'] = atr_percent_vote(data, indicators['atr_percent'])
    if indicators['volume']['enabled']:
        votes['volume'] = volume_vote(data, indicators['volume'])
    return votes

def get_required_signals(enabled_count, min_signals):
    '''quanti indicatori devono essere d'accordo, in base a min_signals del profilo'''
    if min_signals == 'all':
        return enabled_count
    return min_signals

def decide(votes, min_signals):
    '''
    conta i voti e decide la direzione.
    Restituisce (direzione, nomi degli indicatori d'accordo, quanti indicatori sono accesi).
    La direzione è None se nessuna direzione raggiunge il minimo richiesto,
    oppure se lo raggiungono entrambe (segnali contrastanti).
    '''
    long_indicators = []
    short_indicators = []
    for name, vote in votes.items():
        if vote == Signal.LONG or vote == Signal.BOTH:
            long_indicators.append(name)
        if vote == Signal.SHORT or vote == Signal.BOTH:
            short_indicators.append(name)

    enabled_count = len(votes)
    if enabled_count == 0:
        return None, [], 0
    required = get_required_signals(enabled_count, min_signals)

    is_long = len(long_indicators) >= required
    is_short = len(short_indicators) >= required
    if is_long and not is_short:
        return Signal.LONG, long_indicators, enabled_count
    if is_short and not is_long:
        return Signal.SHORT, short_indicators, enabled_count
    return None, [], enabled_count
