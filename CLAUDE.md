# CLAUDE.md — Trading Station

Questo file guida Claude (e me stesso) nello sviluppo del progetto.
Va letto per intero prima di ogni modifica.

---

## 1. Regola più importante: codice SEMPLICE

L'autore del progetto **non è un programmatore esperto** e vuole capire e controllare
ogni riga. Per questo:

- **Semplicità prima di tutto.** Meglio 10 righe chiare che 3 righe "furbe".
- **Funzioni normali** dove possibile. Usare classi solo quando servono davvero
  (es. `Exchange`, `OrderManager`, già presenti).
- **Niente costrutti avanzati** se non indispensabili: niente `async`, decoratori custom,
  metaclassi, generatori complessi, list/dict comprehension annidate, lambda lunghe,
  ereditarietà a più livelli, type hint complicati.
- **Niente import con `*`** nel codice nuovo (`from x import *`): importare per nome,
  così si capisce da dove arriva ogni funzione.
- **Nomi espliciti** in inglese per variabili e funzioni (`latest_rsi`, non `lr`).
- **Commenti e messaggi di log in italiano**, brevi, che spiegano il *perché*.
- **Funzioni corte**, una cosa sola per funzione.
- **Nessuna nuova dipendenza** senza chiedere prima e spiegare a cosa serve.
- **Un passo alla volta**: modifiche piccole, una funzionalità per volta.
- **Spiegare sempre** cosa si è cambiato e perché, in parole semplici.
- **Non fare commit né push** senza richiesta esplicita. Non toccare file che non
  riguardano il compito richiesto.

---

## 2. Visione del progetto

Una "stazione di trading" da terminale, divisa in tre livelli che arriveranno in ordine:

1. **Spotter (avvisi)** — scansiona i mercati, calcola una serie di indicatori
   **attivabili/disattivabili** e invia avvisi (console + Telegram) quando le
   condizioni scelte si verificano. Nessun ordine viene inviato.
2. **Manuale (reazione agli avvisi)** — dall'avviso si può aprire velocemente
   un ordine manuale (market / limit, poi stop loss e take profit).
3. **Automatico (motore)** — le strategie inviano ordini da sole, con limiti di
   rischio chiari e possibilità di avviarle/fermarle.

**Exchange di riferimento: Kraken.** Il codice però deve restare il più possibile
generico grazie a `ccxt` (il nome dell'exchange è un parametro, non va scritto
"a mano" nella logica).

---

## 3. Struttura attuale

```
main.py                     Punto di ingresso: chiede la modalità (prompt_toolkit)
config.py                   Chiavi API, token Telegram, exchange (NON versionato, in .gitignore)
settings.py                 Impostazioni di trading: timeframe, pausa, volume, INDICATORS, MIN_SIGNALS (versionato)
logger.py                   Logger: file + console + Telegram (livello WARNING)

alerts/
  telegram_alert.py         Invia un messaggio Telegram (requests)
  telegram_handler.py       Handler di logging che inoltra a Telegram

utils/
  exchange_manager.py       Classe Exchange: crea l'istanza ccxt (+ xStocks su Kraken)
  data_fetcher.py           Scarica candele (OHLCV), lista simboli, filtro per volume
  completers.py             Autocompletamento per i prompt

signals/
  indicators.py             Calcolo indicatori (RSI, SAR, volatilità oraria, ATR relativo): restituiscono serie di valori
  signals_generator.py      Trasforma un indicatore in un segnale (es. OVERSOLD)
  signal_types.py           Costanti dei segnali (BUY, SELL, OVERBOUGHT, LONG, SHORT, BOTH, ...)
  votes.py                  Voto di ogni indicatore acceso + conteggio (decide LONG/SHORT)

strategies/
  base_strategy.py          BaseStrategy + Valubot (non più usata dallo spotter: sostituita da votes.py)

modes/
  spotter_mode.py           Ciclo infinito: per ogni simbolo scarica dati e conta i voti degli indicatori
  manual_mode.py            Esegue un ordine market / limit / cancel
  closing_mode.py           "Shutter": piazza take profit su tutte le posizioni aperte

docs/
  letteratura.md            Cosa dice la ricerca su ogni indicatore: evidenza, ridondanze, priorità

orders/
  ordermanager.py           Ordini: market, limit, cancella, ordini aperti
  positionmanager.py        Posizioni aperte e chiusura a percentuale

```

Flusso attuale dello spotter:
`main.py` → `spotter()` → `fetch_symbols` → (filtro volume) → loop:
`fetch_market_data` → `get_votes` → `decide` → (se c'è un segnale) `logger.warning` → Telegram.

Esempio di avviso: `SHORT su ADA/USD:USD a 0.24594 - 2 indicatori su 3 (sar, volatility)`

Il meccanismo degli avvisi è semplice e funziona bene: **un `logger.warning(...)`
diventa automaticamente un messaggio Telegram.** `logger.info` resta solo in console/file.

---

## 4. Come si avvia

- Gestore dipendenze: **uv** (`pyproject.toml`, `uv.lock`). Ambiente in `.venv/`.
- Python **3.10** o superiore; la versione usata è scritta in `.python-version`
  e uv la installa da solo se manca.
- TA-Lib si installa da PyPI (versione 0.6 o superiore, wheel già pronte).
- Installazione: `uv sync`
- Avvio: `uv run python main.py`
- Aggiungere / togliere una libreria: `uv add nome` / `uv remove nome`
- Serve un file `config.py` nella radice con questa forma (valori veri mai nel repo):

```python
API_KEYS = {
    'krakenfutures': {'api_key': '', 'api_secret': ''},
}
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''
EXCHANGE_NAME = 'krakenfutures'   # 'kraken' per lo spot
MARKET_TYPE = 'swap'              # 'spot' se EXCHANGE_NAME = 'kraken'
```

Il modello completo è in `config_example.py`.

Il log completo finisce in `trading_station.log` (ignorato da git; può diventare
molto grande, si può cancellare senza problemi).

---

## 5. Problemi noti (da sistemare con calma, uno per volta)

Quelli risolti sono barrati.

1. ~~**Exchange scritto nel codice**~~ — RISOLTO: ora si sceglie con `EXCHANGE_NAME` in `config.py`.
2. ~~**Filtro simboli legato a Binance/Bybit**~~ — RISOLTO: `fetch_symbols` ora ha i
   parametri `market_type`, `quote` e `category` (crypto / tradfi / all).
3. ~~**Crash nel filtro volume**~~ — RISOLTO: i simboli senza dato di volume
   (`quoteVolume` = `None`) vengono saltati.
4. ~~**Strategia fissa**~~ — RISOLTO: indicatori accesi/spenti in `settings.py` (`INDICATORS`)
   e numero minimo di indicatori d'accordo (`MIN_SIGNALS`). Con `'all'` equivale a Valubot (verificato).
5. ~~**Indicatori modificano il DataFrame**~~ — RISOLTO: ogni funzione in `indicators.py`
   restituisce la serie di valori e non aggiunge colonne (regola scritta in cima al file).
6. ~~**Volatilità**~~ — RISOLTO: è la volatilità **oraria** (0.013 = 1,3% all'ora). Prima
   moltiplicava sempre per √60, giusto solo con candele da 1m: con 15m o 1h risultava
   gonfiata di 4-8 volte. Ora la scala si ricava dalla durata delle candele.
7. **`check_reduce_only_order`** esce dal ciclo al primo ordine (il `return False`
   nell'`else` interrompe il `for`) e non distingue take profit da stop loss.
8. **Valori di default mutabili** `params={}` in `OrderManager`: meglio `params=None`.
9. **Modalità shutter/positions** pensata per futures (Bybit): su Kraken spot non ci
   sono "posizioni" nello stesso senso.
10. ~~**Dipendenze da ripulire**~~ — RISOLTO: tolte `logging`, `seaborn`,
    `scikit-learn`, `ipykernel`; aggiunta `requests`.
11. ~~**Spotter senza pausa**~~ — RISOLTO: pausa tra un giro e l'altro e timeframe
    configurabili in `settings.py` (`PAUSE_SECONDS`, `TIMEFRAME`, `CANDLES_LIMIT`).
12. ~~**Errore nel ciclo = spotter fermo**~~ — RISOLTO: `check_symbol()` gestisce gli
    errori del singolo simbolo, lo salta e prosegue (scritto come INFO, non va su Telegram).
13. ~~Commento "don't know if others than bybit works" in `main.py`~~ — RISOLTO:
    la connessione a Kraken funziona (anche senza chiavi API).
14. ~~**Filtro volume lento**~~ — RISOLTO: `fetch_all_tickers()` scarica tutti i ticker
    con una sola richiesta (meno di 1 secondo). Soglia in `settings.py` (`MIN_VOLUME`, 1 milione $).
15. **Ordini sui mercati tradfi non ancora verificati** (azioni, oro, forex...):
    da controllare in Fase 2 (su Kraken spot probabilmente serve `asset_class`).
16. **Shutter e posizioni su Kraken Futures non verificati**: `percent_closing` e
    `check_reduce_only_order` sono stati scritti per Bybit.
17. ~~**Mercati fermi danno falsi segnali**~~ — RISOLTO: `check_symbol` salta i simboli
    con meno di `MIN_ACTIVE_CANDLES` candele mosse nelle ultime `ACTIVITY_CANDLES`
    (`settings.py`, 10 su 60). Su 1m sono saltati ~127 perpetual su 204: hanno pochissimi scambi.
18. ~~**Simbolo senza candele**~~ — RISOLTO: saltato prima di calcolare gli indicatori.
    A fine giro lo spotter scrive quanti simboli ha controllato e quanti ha saltato.

---

## 6. Roadmap

### Fase 0 — Rimettere in piedi la base
- [x] `config.py`: aggiungere `EXCHANGE_NAME`; creare un `config_example.py` versionato
      (senza segreti) come modello.
- [x] Rendere `fetch_symbols` generico (tipo mercato e valuta quote come parametri).
- [x] Aggiungere le azioni tokenizzate di Kraken (xStocks) e la scelta crypto/tradfi/all
      nello spotter.
- [x] Passare ai perpetual: `EXCHANGE_NAME = 'krakenfutures'`, `MARKET_TYPE = 'swap'`.
- [x] Correggere il crash del filtro volume.
- [x] Pulire `pyproject.toml` (punto 10 sopra).
- [ ] Verificare che lo spotter giri su Kraken **senza chiavi API** (i dati di mercato
      sono pubblici: le chiavi servono solo per gli ordini).

### Fase 1 — Spotter con indicatori attivabili
Come funziona (implementato in `signals/votes.py`):

- Ogni indicatore è **una funzione** in `signals/signals_generator.py` che riceve
  il DataFrame e restituisce un segnale (o `None`).
- Un file di impostazioni (es. `settings.py`) contiene un dizionario leggibile:

  ```python
  INDICATORS = {
      'rsi':        {'enabled': True,  'overbought': 70, 'oversold': 30},
      'volatility': {'enabled': True,  'period': 60, 'threshold': 0.013},
      'sar':        {'enabled': False},
  }
  ```

- Lo spotter, per ogni simbolo, calcola solo gli indicatori con `enabled: True`
  e invia un avviso quando le condizioni scelte sono soddisfatte.
- [x] Timeframe configurabile e filtro volume veloce (`settings.py`).
- [x] Stile unico degli indicatori e volatilità oraria indipendente dal timeframe.
- [x] ATR relativo (`'atr'` in `INDICATORS`, spento di default): alternativa a `volatility`
      che confronta ogni simbolo con se stesso. Soglia 1.5 superata ~10% delle volte
      (misurato su 1m e 15m), distribuita su molti simboli invece che sempre sui soliti.
- [x] Niente avvisi ripetuti: stesso simbolo e stessa direzione non vengono reinviati prima di
      `ALERT_COOLDOWN_MINUTES` (60). Se la direzione cambia l'avviso parte subito.
      La memoria degli avvisi si azzera al riavvio dello spotter.
- [ ] Da osservare: il SAR può ribaltarsi LONG/SHORT su una candela ancora in corso
      (visto su QNT, stesso prezzo a pochi secondi di distanza) e far ripartire l'avviso.
      Se diventa fastidioso: cooldown per simbolo indipendente dalla direzione, oppure
      calcolare gli indicatori solo sulle candele chiuse (escludendo l'ultima, ancora in corso).
- [x] Indicatori attivabili (`INDICATORS`) e combinazione: tutti (`MIN_SIGNALS = 'all'`)
      oppure almeno N (`MIN_SIGNALS = 2`). Avviso tipo "3 indicatori su 5".
- [ ] SAR vota sempre (LONG o SHORT) e la volatilità vota BOTH: con `MIN_SIGNALS` basso
      SAR + volatilità bastano da soli a generare molti avvisi. Valutare se il SAR debba
      votare solo all'inversione e se la volatilità debba essere un filtro invece che un voto.
- In seguito: attivare/disattivare indicatori dal prompt senza modificare il file.

- [x] Modi di voto (`'mode'` in `INDICATORS`): lo stesso indicatore può votare in modi diversi.
      RSI: `'reversal'` (ipervenduto = LONG) o `'trend'` (sopra 50 = LONG).
      SAR: `'direction'` (vota sempre) o `'flip'` (vota solo se si è girato nelle ultime
      `flip_candles` candele). Si possono mescolare apposta (es. trend + inversione =
      "compra il ribasso dentro un trend").

#### Nuovi indicatori (vedi `docs/letteratura.md`)
- [x] Documento con la letteratura verificata su indicatori di trend, oscillatori,
      volatilità, volume e dati dei perpetual (funding rate, open interest).
- [ ] Strumento di valutazione dei segnali: cosa fa il prezzo dopo ogni segnale,
      confronto con segnali casuali, al netto delle commissioni, su due periodi diversi.
- [ ] Aggiungere, uno alla volta e solo dopo averli misurati: medie mobili, volume anomalo,
      ADX come filtro, rottura di canale, funding rate.
- Regola: **un indicatore per gruppo** (vedi tabella delle ridondanze nel documento),
  per non far votare più volte la stessa idea.

### Fase 2 — Ordini manuali in reazione agli avvisi
- Dall'avviso proporre un ordine precompilato (simbolo, lato) da confermare a mano.
- Stop loss e take profit adattati a Kraken.
- Sempre una **conferma esplicita** prima di inviare un ordine reale.

### Fase 3 — Motore automatico
- Le strategie (`strategies/`) restituiscono BUY/SELL e un modulo esegue gli ordini.
- Limiti di rischio obbligatori (importo massimo, numero massimo di posizioni).
- Prima in modalità "prova" (solo log, nessun ordine), poi reale.

---

## 7. Note su Kraken e ccxt

- **Kraken è diviso in due exchange ccxt**, con chiavi API diverse:
  - `krakenfutures` = perpetual e futures → **quello usato dal progetto**;
  - `kraken` = spot (a pronti).
- I mercati si scelgono con due impostazioni in `config.py`: `EXCHANGE_NAME` e
  `MARKET_TYPE` (`'swap'` = perpetual). Non c'è un prompt: si cambiano lì.

### Kraken Futures (perpetual)
- ~200-280 perpetual lineari (il numero varia: Kraken aggiunge e toglie mercati), quotati e regolati in USD. Simboli tipo `BTC/USD:USD`
  (la parte dopo `:` è la valuta di regolamento).
- Ci sono anche 4 contratti **inversi** (`BTC/USD:BTC`, regolati in crypto):
  `fetch_symbols` li esclude.
- Ogni mercato ha un campo `info['category']` (DeFi, Meme, AI, Layer 1, xStocks,
  Equities, Indices, Commodities, Forex, Pre-IPO, ...). Le categorie elencate in
  `TRADFI_CATEGORIES` (`utils/data_fetcher.py`) sono considerate `tradfi`, il resto `crypto`.
  Esempi tradfi: `AAPLX/USD:USD`, `SPYX/USD:USD`, `US100/USD:USD`, `XAU/USD:USD` (oro),
  `WTIOIL/USD:USD`, `EUR/USD:USD`.
- Il ticker **non fornisce `quoteVolume`**: `get_quote_volume()` lo calcola come
  `baseVolume * last`.
- Restituisce fino a 1000 candele per richiesta.

### Kraken spot
- Simboli tipo `BTC/USD`, `ETH/EUR`.
- **Azioni tokenizzate (xStocks)**, es. `AAPLX/USD` (~177 coppie in USD). ccxt **non le carica da solo**:
  - `Exchange.add_kraken_stocks()` le chiede con `fetch_markets({'aclass_base': 'tokenized_asset'})`
    e le unisce agli altri mercati;
  - per candele e ticker serve il parametro `{'asset_class': 'tokenized_asset'}`,
    aggiunto in automatico da `get_request_params()`;
  - si riconoscono da `market['info']['aclass_base'] == 'tokenized_asset'`.
- Restituisce al massimo **720 candele** per richiesta.

### In generale
- I mercati azionari fuori dall'orario di borsa USA hanno pochi scambi: il prezzo può
  restare fermo per ore, e indicatori come la volatilità ne risentono.
- Kraken ha limiti di richieste piuttosto stretti: tenere `enableRateLimit: True`
  e non fare cicli senza pausa.
- Per restare generici: usare **solo metodi ccxt unificati** (`fetch_ohlcv`,
  `fetch_ticker`, `create_order`, ...) e controllare `exchange.ccxt.has[...]`
  prima di usare funzioni che non tutti gli exchange supportano.

---

## 8. Sicurezza

- **Mai** scrivere chiavi API o token nel codice versionato né mostrarli nell'output.
- `config.py` resta in `.gitignore`.
- Per le prove con ordini veri usare importi minimi; nessun ordine reale senza
  conferma esplicita dell'utente.

---

## 9. Flusso di lavoro con git

- Un branch per argomento, con il numero della issue GitHub
  (es. `13-evaluate-input`), poi Pull Request su `main`.
- Messaggi di commit brevi e chiari (es. `fix: ...`, `add: ...`, `refactor: ...`).
- Repository: https://github.com/ghiaccionove/tradingstation
