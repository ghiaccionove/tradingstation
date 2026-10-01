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
config.py                   Chiavi API e token Telegram (NON versionato, in .gitignore)
logger.py                   Logger: file + console + Telegram (livello WARNING)

alerts/
  telegram_alert.py         Invia un messaggio Telegram (requests)
  telegram_handler.py       Handler di logging che inoltra a Telegram

utils/
  exchange_manager.py       Classe Exchange: crea l'istanza ccxt (+ xStocks su Kraken)
  data_fetcher.py           Scarica candele (OHLCV), lista simboli, filtro per volume
  completers.py             Autocompletamento per i prompt

signals/
  indicators.py             Calcolo indicatori (RSI, SAR parabolico, volatilità) con TA-Lib
  signals_generator.py      Trasforma un indicatore in un segnale (es. OVERSOLD)
  signal_types.py           Costanti dei segnali (BUY, SELL, OVERBOUGHT, ...)

strategies/
  base_strategy.py          BaseStrategy + Valubot (RSI + volatilità + SAR)

modes/
  spotter_mode.py           Ciclo infinito: per ogni simbolo scarica dati e valuta Valubot
  manual_mode.py            Esegue un ordine market / limit / cancel
  closing_mode.py           "Shutter": piazza take profit su tutte le posizioni aperte

orders/
  ordermanager.py           Ordini: market, limit, cancella, ordini aperti
  positionmanager.py        Posizioni aperte e chiusura a percentuale

libs/                       Wheel di TA-Lib per Windows / Python 3.10
```

Flusso attuale dello spotter:
`main.py` → `spotter()` → `fetch_symbols` → (filtro volume) → loop:
`fetch_market_data` → `Valubot.generate_signal` → `logger.warning` → Telegram.

Il meccanismo degli avvisi è semplice e funziona bene: **un `logger.warning(...)`
diventa automaticamente un messaggio Telegram.** `logger.info` resta solo in console/file.

---

## 4. Come si avvia

- Gestore dipendenze: **Poetry** (`pyproject.toml`, `poetry.lock`).
- Python **3.10** (la wheel di TA-Lib in `libs/` è per cp310 su Windows).
- Installazione: `poetry install`
- Avvio: `poetry run python main.py`
- Serve un file `config.py` nella radice con questa forma (valori veri mai nel repo):

```python
API_KEYS = {
    'kraken': {'api_key': '', 'api_secret': ''},
}
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''
```

Il log completo finisce in `trading_station.log` (ignorato da git; può diventare
molto grande, si può cancellare senza problemi).

---

## 5. Problemi noti (da sistemare con calma, uno per volta)

Quelli risolti sono barrati.

1. ~~**Exchange scritto nel codice**~~ — RISOLTO: ora si sceglie con `EXCHANGE_NAME` in `config.py`.
2. ~~**Filtro simboli legato a Binance/Bybit**~~ — RISOLTO: `fetch_symbols` ora ha i
   parametri `market_type`, `quote` e `category` (crypto / stocks / all).
3. ~~**Crash nel filtro volume**~~ — RISOLTO: i simboli senza dato di volume
   (`quoteVolume` = `None`) vengono saltati.
4. **Strategia fissa**: lo spotter usa sempre `Valubot`; gli indicatori non si
   possono attivare/disattivare.
5. **Indicatori modificano il DataFrame** aggiungendo colonne (`data['rsi'] = ...`).
   Funziona, ma va deciso uno stile unico (vedi commento in `indicators.py`).
6. **Volatilità**: il commento dice "annualizzata" ma il calcolo usa `sqrt(60)`;
   chiarire cosa si vuole misurare.
7. **`check_reduce_only_order`** esce dal ciclo al primo ordine (il `return False`
   nell'`else` interrompe il `for`) e non distingue take profit da stop loss.
8. **Valori di default mutabili** `params={}` in `OrderManager`: meglio `params=None`.
9. **Modalità shutter/positions** pensata per futures (Bybit): su Kraken spot non ci
   sono "posizioni" nello stesso senso.
10. ~~**Dipendenze da ripulire**~~ — RISOLTO: tolte `logging`, `seaborn`,
    `scikit-learn`, `ipykernel`; aggiunta `requests`.
11. ~~**Spotter senza pausa**~~ — RISOLTO: pausa tra un giro e l'altro
    (`pause_seconds`, predefinito 60). Resta da rendere configurabile il timeframe:
    ora scarica sempre candele da 1 minuto (Kraken ne restituisce al massimo 720).
12. ~~**Errore nel ciclo = spotter fermo**~~ — RISOLTO: `check_symbol()` gestisce gli
    errori del singolo simbolo, lo salta e prosegue (scritto come INFO, non va su Telegram).
13. ~~Commento "don't know if others than bybit works" in `main.py`~~ — RISOLTO:
    la connessione a Kraken funziona (anche senza chiavi API).
14. **Filtro volume lento**: fa una richiesta per ogni simbolo (con 800 simboli e i limiti
    di Kraken servono diversi minuti). Si potrebbe usare `fetch_tickers` (una sola
    richiesta per tutti). Anche la soglia predefinita (50 milioni) è molto alta per Kraken.
15. **Ordini sulle azioni (xStocks) non ancora verificati**: probabilmente richiedono
    anche loro il parametro `asset_class`, come i dati. Da controllare in Fase 2.

---

## 6. Roadmap

### Fase 0 — Rimettere in piedi la base
- [x] `config.py`: aggiungere `EXCHANGE_NAME`; creare un `config_example.py` versionato
      (senza segreti) come modello.
- [x] Rendere `fetch_symbols` generico (tipo mercato e valuta quote come parametri).
- [x] Aggiungere le azioni tokenizzate di Kraken (xStocks) e la scelta crypto/stocks/all
      nello spotter.
- [x] Correggere il crash del filtro volume.
- [x] Pulire `pyproject.toml` (punto 10 sopra).
- [ ] Verificare che lo spotter giri su Kraken **senza chiavi API** (i dati di mercato
      sono pubblici: le chiavi servono solo per gli ordini).

### Fase 1 — Spotter con indicatori attivabili
Idea semplice, senza architetture complicate:

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
- Aggiungere: timeframe configurabile, pausa tra un giro e l'altro, gestione errori
  per singolo simbolo, niente avvisi ripetuti per lo stesso simbolo a pochi minuti
  di distanza.
- In seguito: attivare/disattivare indicatori dal prompt senza modificare il file.

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

- In ccxt: `ccxt.kraken` = spot, `ccxt.krakenfutures` = futures/perpetual.
  Sono due exchange diversi, con chiavi API diverse.
- Simboli nel formato ccxt unificato (`BTC/USD`, `ETH/EUR`), non quello nativo Kraken
  (`XXBTZUSD`).
- **Azioni (xStocks)**: Kraken offre azioni tokenizzate (es. `AAPLX/USD`, `TSLAX/USD`),
  ~177 coppie in USD. ccxt **non le carica da solo**:
  - `Exchange.add_kraken_stocks()` le chiede con `fetch_markets({'aclass_base': 'tokenized_asset'})`
    e le unisce agli altri mercati;
  - per candele e ticker serve il parametro `{'asset_class': 'tokenized_asset'}`,
    aggiunto in automatico da `get_request_params()` in `utils/data_fetcher.py`;
  - si riconoscono da `market['info']['aclass_base'] == 'tokenized_asset'`
    (funzione `get_market_category()`);
  - fuori dall'orario di borsa USA hanno pochi scambi: il prezzo può restare fermo
    per ore, e indicatori come la volatilità ne risentono.
- Kraken restituisce al massimo **720 candele** per richiesta.
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
