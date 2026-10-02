class Signal:
    BUY = 'BUY'
    SELL = 'SELL'
    HOLD = 'HOLD'
    OVERBOUGHT = 'OVERBOUGHT'
    OVERSOLD = 'OVERSOLD'
    UP = 'UP'
    DOWN = 'DOWN'
    HIGH_VOLATILITY = 'HIGH_VOLATILITY'
    LOW_VOLATILITY = 'LOW_VOLATILITY'

    # voti degli indicatori (usati in signals/votes.py)
    LONG = 'LONG'
    SHORT = 'SHORT'
    BOTH = 'BOTH'      # l'indicatore conferma entrambe le direzioni (es. volatilità alta)
