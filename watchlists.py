# Elenchi di titoli da controllare con la fonte Yahoo (vedi PROFILES in settings.py).
# I simboli sono quelli di Yahoo Finance: si trovano cercando il titolo su finance.yahoo.com.
#   Milano: suffisso .MI (es. ENI.MI)    Xetra: .DE (es. SAP.DE)    Parigi: .PA (es. MC.PA)
#   USA: nessun suffisso (es. AAPL)
# Per aggiungere un titolo basta scriverlo nella lista.

# Grandi titoli della Borsa di Milano (FTSE MIB)
WATCHLIST_ITALIA = [
    'ENI.MI',    # Eni
    'ISP.MI',    # Intesa Sanpaolo
    'UCG.MI',    # UniCredit
    'ENEL.MI',   # Enel
    'STLAM.MI',  # Stellantis
    'RACE.MI',   # Ferrari
    'G.MI',      # Generali
    'STMMI.MI',  # STMicroelectronics
    'LDO.MI',    # Leonardo
    'PRY.MI',    # Prysmian
    'TIT.MI',    # Telecom Italia
    'MB.MI',     # Mediobanca
    'BMPS.MI',   # Monte dei Paschi
    'PST.MI',    # Poste Italiane
    'TEN.MI',    # Tenaris
]

# Grandi titoli USA
WATCHLIST_USA = [
    'AAPL',   # Apple
    'MSFT',   # Microsoft
    'NVDA',   # Nvidia
    'AMZN',   # Amazon
    'GOOGL',  # Alphabet (Google)
    'META',   # Meta
    'TSLA',   # Tesla
    'AMD',    # AMD
    'MU',     # Micron
    'PLTR',   # Palantir
]
