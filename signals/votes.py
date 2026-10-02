'''
Votazione degli indicatori.

Ogni indicatore acceso in settings.py "vota" una direzione:
LONG, SHORT, BOTH (conferma entrambe) oppure None (nessun segnale).
Poi si contano i voti: se abbastanza indicatori sono d'accordo, c'è un segnale.
'''
from signals.signal_types import Signal
from signals.signals_generator import rsi_signal, parabolic_trend, volatility_signal, atr_signal
from settings import INDICATORS, MIN_SIGNALS


# --- Il voto di ogni indicatore ---

def rsi_vote(data, settings):
    signal = rsi_signal(data, overbought=settings['overbought'], oversold=settings['oversold'],
                        period=settings['period'])
    if signal == Signal.OVERSOLD:
        return Signal.LONG
    if signal == Signal.OVERBOUGHT:
        return Signal.SHORT
    return None

def sar_vote(data, settings):
    signal = parabolic_trend(data, acceleration=settings['acceleration'], maximum=settings['maximum'])
    if signal == Signal.UP:
        return Signal.LONG
    return Signal.SHORT

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


# --- Raccolta e conteggio dei voti ---

def get_votes(data):
    '''
    calcola solo gli indicatori accesi e restituisce i loro voti, es.
    {'rsi': 'LONG', 'sar': 'LONG', 'volatility': None}
    Per aggiungere un indicatore: scrivere la sua funzione ..._vote e aggiungere un blocco qui.
    '''
    votes = {}
    if INDICATORS['rsi']['enabled']:
        votes['rsi'] = rsi_vote(data, INDICATORS['rsi'])
    if INDICATORS['sar']['enabled']:
        votes['sar'] = sar_vote(data, INDICATORS['sar'])
    if INDICATORS['volatility']['enabled']:
        votes['volatility'] = volatility_vote(data, INDICATORS['volatility'])
    if INDICATORS['atr']['enabled']:
        votes['atr'] = atr_vote(data, INDICATORS['atr'])
    return votes

def get_required_signals(enabled_count):
    '''quanti indicatori devono essere d'accordo, in base a MIN_SIGNALS'''
    if MIN_SIGNALS == 'all':
        return enabled_count
    return MIN_SIGNALS

def decide(votes):
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
    required = get_required_signals(enabled_count)

    is_long = len(long_indicators) >= required
    is_short = len(short_indicators) >= required
    if is_long and not is_short:
        return Signal.LONG, long_indicators, enabled_count
    if is_short and not is_long:
        return Signal.SHORT, short_indicators, enabled_count
    return None, [], enabled_count
