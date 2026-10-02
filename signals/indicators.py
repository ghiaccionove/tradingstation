'''
Calcolo degli indicatori.

Regola di stile: ogni funzione riceve la tabella delle candele (data) e
RESTITUISCE la serie di valori dell'indicatore, una per candela.
Non modifica la tabella: niente colonne aggiunte.
Per avere l'ultimo valore: rsi(data).iloc[-1]
'''
import talib
import numpy as np

def get_candle_minutes(data):
    '''durata di una candela in minuti, ricavata dagli orari delle candele (timestamp in millisecondi)'''
    # mediana: così eventuali buchi (es. mercato chiuso) non falsano il risultato
    return data['timestamp'].diff().median() / 60000

def volatility(data, period=60):
    '''
    volatilità oraria: di quanto si muove tipicamente il prezzo in un'ora.
    Es. 0.013 = 1,3% all'ora.
    Si calcola la deviazione standard dei rendimenti delle ultime `period` candele
    e la si riporta a un'ora, così il valore non dipende dal timeframe scelto.
    '''
    returns = np.log(data['close'] / data['close'].shift(1))
    candles_per_hour = 60 / get_candle_minutes(data)
    return returns.rolling(period).std() * (candles_per_hour ** 0.5)

def rsi(data, period=14):
    '''RSI (Relative Strength Index): valori da 0 a 100'''
    return talib.RSI(data['close'], timeperiod=period)

def parabolic_sar(data, acceleration=0.02, maximum=0.2):
    '''SAR parabolico: un prezzo per candela, sotto il prezzo in trend rialzista e sopra in ribassista'''
    return talib.SAR(data['high'], data['low'], acceleration=acceleration, maximum=maximum)

def atr_ratio(data, period=14, average_period=100):
    '''
    ATR relativo: confronta la volatilità di adesso con quella normale per QUESTO simbolo.
    - NATR = ATR in percentuale del prezzo: ampiezza media delle ultime `period` candele
      (distanza tra massimo e minimo, contando anche i salti tra una candela e l'altra)
    - il rapporto divide il NATR attuale per la sua media delle ultime `average_period` candele
    Es. 1.0 = volatilità normale, 1.5 = il 50% più agitato del solito.
    Essendo un rapporto non dipende né dal prezzo né dal timeframe.
    '''
    natr = talib.NATR(data['high'], data['low'], data['close'], timeperiod=period)
    return natr / natr.rolling(average_period).mean()
