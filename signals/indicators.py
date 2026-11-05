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

def moving_average(values, period, ma_type='sma'):
    '''media mobile di una linea qualsiasi (RSI, volume, ...). 'sma' = semplice, 'ema' = reagisce prima'''
    if ma_type == 'sma':
        return values.rolling(period, min_periods=period // 2).mean()
    if ma_type == 'ema':
        return values.ewm(span=period, min_periods=period // 2).mean()
    raise ValueError(f"ma_type '{ma_type}' non valido: usare 'sma' o 'ema'")

def volume_line(data):
    '''il volume di ogni candela. Volume zero = dato mancante (es. Yahoo a 1h per la candela delle 9 di Milano)'''
    return data['volume'].replace(0, np.nan)

def average_of_previous_days(volumes, days):
    '''media dei volumi precedenti di una stessa posizione nella giornata (la candela stessa non conta)'''
    return volumes.shift(1).rolling(days, min_periods=days // 2).mean()

def volume_ratio(data, days=20):
    '''
    volume anomalo: volume di ogni candela diviso per la media delle candele nella stessa
    posizione della giornata (es. la prima di ogni giorno) negli ultimi `days` giorni.
    Es. 2.0 = il doppio del normale per quel momento. Serve perché ogni giornata ha il suo andamento:
    sulle azioni USA la prima ora ha di norma 2,5 volte il volume delle altre, senza che sia anomalo.
    Si usa la posizione e non l'orario: con il cambio dell'ora legale l'orario UTC si sposta.
    Volume zero = dato mancante (es. Yahoo a 1h per la candela delle 9 di Milano): lì il risultato resta vuoto.
    '''
    volumes = volume_line(data)
    days_of_candles = data['timestamp'] // 86400000
    position_in_day = volumes.groupby(days_of_candles).cumcount()
    averages = volumes.groupby(position_in_day).transform(average_of_previous_days, days)
    return volumes / averages

def atr_percent(data, period=14):
    '''NATR = ATR in percentuale del prezzo: ampiezza media delle ultime `period` candele, confrontabile tra titoli'''
    return talib.NATR(data['high'], data['low'], data['close'], timeperiod=period)

def atr_ratio(data, period=14, average_period=100):
    '''
    ATR relativo: confronta la volatilità di adesso con quella normale per QUESTO simbolo.
    - NATR = ATR in percentuale del prezzo: ampiezza media delle ultime `period` candele
      (distanza tra massimo e minimo, contando anche i salti tra una candela e l'altra)
    - il rapporto divide il NATR attuale per la sua media delle ultime `average_period` candele
    Es. 1.0 = volatilità normale, 1.5 = il 50% più agitato del solito.
    Essendo un rapporto non dipende né dal prezzo né dal timeframe.
    '''
    natr = atr_percent(data, period=period)
    return natr / natr.rolling(average_period).mean()
