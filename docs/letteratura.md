# Indicatori tecnici: cosa dice la letteratura

Documento di riferimento per scegliere quali indicatori aggiungere allo spotter.
Ogni fonte citata è stata verificata (autori, rivista, anno e risultato principale);
i link sono in fondo. Ultimo aggiornamento: ottobre 2026.

---

## Come leggere questo documento

Per ogni indicatore c'è un **livello di evidenza**, cioè quanto la ricerca accademica
lo supporta:

| Livello | Significato |
|---|---|
| **Forte** | Molti studi, su più mercati e periodi, anche con controlli statistici rigorosi |
| **Moderata** | Alcuni studi positivi, ma su pochi mercati o senza controlli rigorosi |
| **Debole / mista** | Risultati contrastanti, oppure studi pochi e limitati |
| **Assente** | Nessuno studio accademico verificato: è solo pratica dei trader |

"Evidenza forte" **non vuol dire** che l'indicatore funzionerà sui nostri perpetual,
sul nostro timeframe e con le nostre commissioni. Vuol dire solo che vale la pena misurarlo.

---

## 1. Lezioni generali (valgono per tutti gli indicatori)

### 1.1 Le regole semplici possono funzionare...
Brock, Lakonishok e LeBaron (1992) hanno testato medie mobili e rotture di massimi/minimi
sul Dow Jones dal 1897 al 1986: i rendimenti dopo i segnali di acquisto erano più alti
e meno volatili di quelli dopo i segnali di vendita. È lo studio che ha riaperto
l'interesse accademico per l'analisi tecnica.

### 1.2 ...ma attenzione al "data snooping"
Sullivan, Timmermann e White (1999) hanno ripreso lo stesso studio allargandolo a circa
8.000 regole e correggendo per il **data snooping**: se si provano tante regole e si tiene
la migliore, se ne trova sempre una che sembra funzionare per puro caso.
Corretto questo effetto, le regole migliori funzionavano nel periodo originale ma
**non più dopo il 1986**.

> **Per noi**: se proviamo molte combinazioni di indicatori e parametri e teniamo la
> migliore, rischiamo di ingannarci. Ogni regola va provata su un periodo e
> **verificata su un altro periodo** che non abbiamo usato per sceglierla.

### 1.3 Le regole perdono efficacia quando diventano famose
Fang, Jacobsen e Qin (2017) mostrano che le Bande di Bollinger erano molto profittevoli
**prima** della loro introduzione (1983) e hanno perso progressivamente efficacia man mano
che diventavano popolari; dal 2001 (anno del libro di Bollinger) hanno in gran parte perso
potere predittivo sui principali mercati azionari.

> **Per noi**: gli indicatori più famosi (RSI, MACD, Bollinger) sono quelli che
> tutti guardano. Non per questo sono inutili, ma non c'è da aspettarsi miracoli.

### 1.4 La rassegna generale
Park e Irwin (2007) hanno raccolto decine di studi: i primi studi trovavano profitti
nei mercati valutari e dei futures, ma non in quelli azionari; gli studi più moderni sono
in maggioranza positivi, ma spesso con problemi metodologici (data snooping, costi di
transazione, rischio non considerati).

### 1.5 Il timeframe conta molto
Quasi tutti gli studi usano **dati giornalieri o più lunghi**. Sul brevissimo periodo:
Marshall, Cahan e Cahan (2008) hanno testato 7.846 regole tecniche popolari sul mercato
azionario USA **intraday**: **nessuna** è risultata profittevole dopo la correzione per
il data snooping.

> **Per noi**: il timeframe da 1 minuto è il più rumoroso e quello con meno supporto.
> Da 15 minuti in su i segnali hanno più senso; il giornaliero è quello più studiato.

### 1.6 Il trend è la famiglia più solida
- Moskowitz, Ooi e Pedersen (2012) documentano il **time-series momentum**: comprare
  i futures saliti nell'ultimo anno e vendere quelli scesi dà profitti significativi
  su decine di mercati (azioni, valute, materie prime, obbligazioni).
- Hurst, Ooi e Pedersen (2017) estendono l'analisi dal 1880: il trend following ha dato
  rendimenti medi positivi **in ogni decennio** e ha funzionato bene in 8 delle 10 crisi
  peggiori del secolo.

Attenzione: orizzonti di **settimane e mesi**, non di minuti.

---

## 2. Cosa sappiamo sulle crypto

- **Liu e Tsyvinski (2021)**: le crypto hanno un **forte time-series momentum** e i loro
  rendimenti non dipendono dai fattori classici di azioni, valute e materie prime.
- **Detzel e altri (2021)**: il **rapporto tra prezzo e sua media mobile** prevede i
  rendimenti giornalieri del bitcoin, sia nel periodo di stima sia fuori; le strategie
  basate su questi rapporti battono il "compra e tieni".
- **Corbet e altri (2019)**: su rendimenti **ad alta frequenza** del bitcoin, le regole
  a media mobile funzionano (la migliore è la "media mobile a lunghezza variabile"),
  con i segnali di acquisto migliori di quelli di vendita.
- **Grobys, Ahmed e Sapkota (2020)**: su 11 crypto, una semplice regola a media mobile
  (20 giorni) genera rendimenti in eccesso.
- **Hudson e Urquhart (2021)**: quasi 15.000 regole tecniche dalle cinque classi principali
  (le stesse di Sullivan e altri: filtri, medie mobili, supporti e resistenze, rotture
  di canale, on-balance volume) mostrano **prevedibilità e profittabilità significative
  in ogni classe e in ogni crypto** studiata.
- **Fieberg e altri (2025)**: combinando 28 segnali tecnici (momentum, medie mobili,
  volumi, volatilità) su oltre 3.000 crypto si ottiene un fattore di trend ("CTREND")
  che prevede i rendimenti, **resiste ai costi di transazione** e funziona anche sulle
  crypto grandi e liquide.

> **In sintesi**: per le crypto le prove sono più favorevoli che per le azioni,
> soprattutto per **trend e medie mobili**. Restano però studi quasi tutti su dati
> giornalieri, e quasi tutti sul mercato spot, non sui perpetual.

---

## 3. Schede degli indicatori

Legenda della riga "Nel progetto": ✅ già presente · 🟡 candidato · ⛔ sconsigliato.

### Famiglia TREND (seguono la direzione del prezzo)

#### Medie mobili (SMA / EMA): prezzo sopra/sotto la media, incrocio tra due medie
- **Cosa misura**: la direzione del prezzo nel periodo recente.
- **Letteratura**: Brock e altri (1992); Detzel e altri (2021); Corbet e altri (2019);
  Grobys e altri (2020); Hudson e Urquhart (2021).
- **Evidenza**: **Forte** (la più studiata in assoluto, anche sulle crypto).
- **Nel progetto**: 🟡 **primo candidato**.

#### Time-series momentum (rendimento degli ultimi N periodi positivo o negativo)
- **Cosa misura**: se il prezzo è salito o sceso nell'ultimo periodo.
- **Letteratura**: Moskowitz e altri (2012); Hurst e altri (2017); Liu e Tsyvinski (2021).
- **Evidenza**: **Forte**, ma su orizzonti di settimane/mesi.
- **Nel progetto**: 🟡 candidato, simile alle medie mobili (vedi ridondanze).

#### Rottura di canale / Donchian (prezzo oltre il massimo o il minimo delle ultime N candele)
- **Cosa misura**: l'uscita del prezzo da un intervallo, cioè l'inizio di un possibile trend.
- **Letteratura**: "trading range break" in Brock e altri (1992); "channel breakouts"
  tra le classi di Sullivan e altri (1999) e Hudson e Urquhart (2021).
- **Evidenza**: **Moderata**.
- **Nel progetto**: 🟡 candidato. Vota solo nel momento della rottura, quindi più
  "selettivo" del SAR.

#### MACD (differenza tra due medie esponenziali e sua media)
- **Cosa misura**: trend e sua accelerazione. Creato da Gerald Appel a fine anni '70.
- **Letteratura**: Chong e Ng (2008), 60 anni dell'indice FT30 di Londra: le regole MACD
  battono il "compra e tieni" nella maggior parte dei casi. Un solo mercato, senza
  correzione per il data snooping.
- **Evidenza**: **Moderata / debole**.
- **Nel progetto**: 🟡 candidato, ma **molto simile alle medie mobili**: ha senso
  tenerne uno solo dei due (vedi ridondanze).

#### SAR parabolico
- **Cosa misura**: un livello di "stop" che segue il prezzo; sotto il prezzo in trend
  rialzista, sopra in ribassista. Ideato da Wilder (1978) **come sistema di uscita**
  (dove mettere lo stop), non come segnale di entrata.
- **Letteratura**: quasi nessuno studio dedicato. Gurrib (2018) lo usa insieme all'ADX
  sulle principali coppie valutarie (dati settimanali e mensili, 2000-2018): il sistema
  settimanale risulta più affidabile di quello mensile.
- **Evidenza**: **Debole** (come segnale a sé).
- **Nel progetto**: ✅ presente. Vota **sempre** (il prezzo è sempre sopra o sotto il SAR):
  per questo pesa molto nel conteggio dei voti.

#### ADX (forza del trend, senza direzione)
- **Cosa misura**: **quanto è forte** il trend, non se sale o scende (Wilder, 1978).
  Valori alti = trend forte, bassi = mercato laterale.
- **Letteratura**: Gurrib (2018), insieme al SAR (vedi sopra). Altri numeri che circolano
  online (percentuali di successo precise) vengono da blog commerciali e **non sono
  stati verificati**.
- **Evidenza**: **Debole**.
- **Nel progetto**: 🟡 interessante **come filtro** invece che come voto: per esempio
  "fai contare SAR e medie mobili solo quando l'ADX indica un trend forte".
  Potrebbe essere la risposta al problema del SAR che vota sempre.

### Famiglia OSCILLATORI (cercano eccessi e inversioni)

#### RSI
- **Cosa misura**: la velocità dei rialzi rispetto ai ribassi recenti, da 0 a 100.
  Sopra 70 "ipercomprato", sotto 30 "ipervenduto" (Wilder, 1978).
- **Letteratura**: Chong e Ng (2008) lo trovano profittevole sull'FT30 insieme al MACD.
  Va notato che è una logica **contraria al trend** (compra quando è sceso molto),
  mentre sulle crypto le prove più solide riguardano il trend.
- **Evidenza**: **Debole / mista**.
- **Nel progetto**: ✅ presente.

#### Bande di Bollinger
- **Cosa misura**: un canale di 2 deviazioni standard attorno a una media mobile.
  Uso classico: prezzo sulla banda inferiore = ipervenduto. Uso alternativo:
  rottura della banda = inizio di un movimento.
- **Letteratura**: Lento, Gradojevic e Wright (2007): l'uso classico **non batte** il
  "compra e tieni"; la versione **opposta** (contraria) dà invece rendimenti positivi
  in vari mercati. Fang e altri (2017): efficacia persa con la popolarità.
- **Evidenza**: **Debole / mista**.
- **Nel progetto**: 🟡 possibile, ma va deciso **quale** uso (inversione o rottura).
  L'ampiezza delle bande è invece un indicatore di volatilità (simile all'ATR).

#### Stocastico, CCI, Williams %R
- **Cosa misurano**: la posizione del prezzo rispetto al suo intervallo o alla sua media
  recente. Per costruzione misurano **quasi la stessa cosa dell'RSI**.
- **Letteratura**: nessuno studio accademico verificato.
- **Evidenza**: **Assente**.
- **Nel progetto**: ⛔ sconsigliati: aggiungerli farebbe votare più volte la stessa idea.

### Famiglia VOLATILITÀ (quanto si muove il prezzo, senza direzione)

#### Volatilità (deviazione standard dei rendimenti) e ATR relativo
- **Cosa misurano**: l'ampiezza dei movimenti. L'ATR è di Wilder (1978).
- **Letteratura**: Moreira e Muir (2017) mostrano che la volatilità è utile per
  **gestire il rischio** (ridurre l'esposizione quando è alta migliora i risultati),
  non per prevedere la direzione.
- **Evidenza**: **Forte come gestione del rischio**, **assente come segnale di direzione**.
- **Nel progetto**: ✅ entrambi presenti. Il loro uso naturale è come **filtro**
  ("guarda solo i mercati in movimento") e, in Fase 2-3, per dimensionare stop loss e
  quantità.

### Famiglia VOLUME

#### Volume anomalo (volume molto sopra la sua media)
- **Cosa misura**: un'attività di scambi insolita.
- **Letteratura**:
  - Blume, Easley e O'Hara (1994): il volume contiene informazioni che **non si possono
    ricavare dal prezzo** (modello teorico).
  - Gervais, Kaniel e Mingelgrin (2001): le azioni con volume insolitamente alto in un
    giorno o una settimana tendono a salire nel mese successivo.
  - Lee e Swaminathan (2000): il volume passato influenza forza e durata del momentum.
  - Bouri e altri (2019), su 7 crypto con dati giornalieri: il volume aiuta a prevedere
    i **rendimenti estremi**, sia positivi sia negativi.
- **Evidenza**: **Moderata** (soprattutto come conferma).
- **Nel progetto**: 🟡 **secondo candidato**. Porta un'informazione che oggi non abbiamo:
  tutti gli indicatori attuali usano solo il prezzo.

#### OBV (On-Balance Volume)
- **Cosa misura**: somma il volume dei giorni di rialzo e sottrae quello dei giorni di
  ribasso (Granville, 1963). L'idea è che il volume anticipi il prezzo.
- **Letteratura**: Tsang e Chong (2009): regola OBV profittevole nei mercati azionari
  della "Grande Cina". È tra le cinque classi di Sullivan e altri (1999) e di Hudson e
  Urquhart (2021).
- **Evidenza**: **Moderata / debole**.
- **Nel progetto**: 🟡 candidato in alternativa al volume anomalo.

#### MFI, Chaikin Money Flow, VWAP
- **MFI**: è un RSI che tiene conto del volume. **Chaikin Money Flow**: dove chiude il
  prezzo dentro la candela, pesato per il volume. **VWAP**: prezzo medio pesato per
  il volume, nato come riferimento per eseguire ordini; sulle crypto (mercato 24/7,
  senza apertura e chiusura) va "ancorato" a un orario scelto.
- **Letteratura**: nessuno studio accademico verificato come segnale. Fieberg e altri
  (2025) includono indicatori di volume nel loro fattore CTREND, ma combinati con altri
  tramite machine learning.
- **Evidenza**: **Assente** (come segnali singoli).
- **Nel progetto**: da valutare dopo volume anomalo e OBV.

### Famiglia PERPETUAL (dati che esistono solo per i perpetual)

#### Funding rate
- **Cosa misura**: il pagamento periodico tra chi è long e chi è short, che mantiene il
  prezzo del perpetual vicino a quello spot. Funding alto e positivo = molti long che
  pagano = mercato sbilanciato al rialzo.
- **Letteratura**: He, Manela, Ross e von Wachter (2022) descrivono il meccanismo.
  Studi sulla capacità del funding di **prevedere i prezzi**: non ne ho trovati di
  verificati e consolidati.
- **Evidenza**: **Assente** come segnale, ma è un'informazione unica e diversa dal prezzo.
- **Su Kraken**: disponibile tramite ccxt, attuale e storico (`fetch_funding_rates`,
  `fetch_funding_rate_history`), pagato **ogni ora**.
- **Nel progetto**: 🟡 candidato sperimentale, da misurare prima di usarlo.

#### Open interest
- **Cosa misura**: quanti contratti sono aperti. Se sale insieme al prezzo indica nuovi
  soldi che entrano nel trend.
- **Letteratura**: nessuno studio verificato come segnale.
- **Su Kraken**: solo il **valore attuale** (dentro il ticker), **niente storico**
  tramite ccxt. Per usarlo dovremmo salvarlo noi nel tempo.
- **Nel progetto**: per ora ⛔ non praticabile.

---

## 4. Ridondanze: chi misura la stessa cosa

Nel nostro sistema di voti, due indicatori che misurano la stessa cosa contano come due
voti, ma sono **una sola opinione**. Gruppi di indicatori simili:

| Gruppo | Indicatori | Consiglio |
|---|---|---|
| Direzione del trend | Medie mobili, MACD, time-series momentum, SAR | Tenerne **uno o due**, non tutti |
| Eccessi / inversione | RSI, Stocastico, CCI, Williams %R, MFI, Bollinger (uso classico) | Tenerne **uno** |
| Volatilità | Volatilità, ATR relativo, ampiezza di Bollinger | Tenerne **uno** |
| Forza del trend | ADX | Unico nel suo genere (meglio come filtro) |
| Volume | Volume anomalo, OBV, Chaikin, VWAP | Tenerne **uno** |
| Posizionamento | Funding rate, open interest | Unici, solo perpetual |

Un buon insieme di indicatori ne prende **uno per gruppo**: così "3 su 4" vuol dire
davvero tre informazioni diverse d'accordo tra loro.

---

## 5. Conclusioni per il progetto

1. **Priorità di aggiunta**, in base a evidenza e informazione nuova portata:
   1. **Medie mobili** (rapporto prezzo/media o incrocio) — evidenza forte, anche crypto.
   2. **Volume anomalo** — informazione oggi assente, evidenza moderata.
   3. **ADX come filtro** — potrebbe rendere utile il SAR invece di farlo votare sempre.
   4. **Rottura di canale (Donchian)** — trend "selettivo".
   5. **Funding rate** — sperimentale, unico dei perpetual.
2. **Da non aggiungere**: altri oscillatori simili all'RSI.
3. **Ogni nuovo indicatore va misurato** sui dati di Kraken prima di diventare un voto,
   provando su un periodo e verificando su un altro (lezione del data snooping).
   → serve lo **strumento di valutazione dei segnali** (prossimo passo).
4. **Timeframe**: la letteratura sostiene molto più i timeframe lunghi (da 15 minuti
   in su, meglio orari o giornalieri) che quello da 1 minuto.

---

## 6. Letture consigliate sul SAR (e su Wilder in generale)

- **Wilder (1978)**, *New Concepts in Technical Trading Systems*: il libro originale in cui
  nascono RSI, SAR, ATR e ADX. Utile per capire **per cosa** erano pensati (il SAR come
  sistema di stop, l'ADX per sapere quando seguire il trend).
- **Gurrib (2018)**: un esempio accademico di SAR usato insieme all'ADX.

---

## 7. Bibliografia

- Blume, L., Easley, D., O'Hara, M. (1994). Market Statistics and Technical Analysis: The Role of Volume. *Journal of Finance*, 49(1), 153-181. [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1994.tb04424.x)
- Bouri, E., Lau, C. K., Lucey, B. M., Roubaud, D. (2019). Trading volume and the predictability of return and volatility in the cryptocurrency market. *Finance Research Letters*, 29, 340-346. [IDEAS](https://ideas.repec.org/a/eee/finlet/v29y2019icp340-346.html)
- Brock, W., Lakonishok, J., LeBaron, B. (1992). Simple Technical Trading Rules and the Stochastic Properties of Stock Returns. *Journal of Finance*, 47(5), 1731-1764. [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1992.tb04681.x)
- Chong, T. T. L., Ng, W. K. (2008). Technical analysis and the London stock exchange: testing the MACD and RSI rules using the FT30. *Applied Economics Letters*, 15(14), 1111-1114. [EconPapers](https://econpapers.repec.org/RePEc:taf:apeclt:v:15:y:2008:i:14:p:1111-1114)
- Corbet, S., Eraslan, V., Lucey, B., Sensoy, A. (2019). The effectiveness of technical trading rules in cryptocurrency markets. *Finance Research Letters*, 31, 32-37. [EconPapers](https://econpapers.repec.org/article/eeefinlet/v_3a31_3ay_3a2019_3ai_3ac_3ap_3a32-37.htm)
- Detzel, A., Liu, H., Strauss, J., Zhou, G., Zhu, Y. (2021). Learning and Predictability via Technical Analysis: Evidence from Bitcoin and Stocks with Hard-to-Value Fundamentals. *Financial Management*, 50(1), 107-137.
- Fang, J., Jacobsen, B., Qin, Y. (2017). Popularity versus Profitability: Evidence from Bollinger Bands. *Journal of Portfolio Management*, 43(4), 152-159. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2484322)
- Fieberg, C., Liedtke, G., Poddig, T., Walker, T., Zaremba, A. (2025). A Trend Factor for the Cross Section of Cryptocurrency Returns. *Journal of Financial and Quantitative Analysis*, 60(7). [Cambridge](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/trend-factor-for-the-cross-section-of-cryptocurrency-returns/4C1509ACBA33D5DCAF0AC24379148178)
- Gervais, S., Kaniel, R., Mingelgrin, D. (2001). The High-Volume Return Premium. *Journal of Finance*, 56(3), 877-919. [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00349)
- Granville, J. (1963). *Granville's New Key to Stock Market Profits*. (Origine dell'OBV.)
- Grobys, K., Ahmed, S., Sapkota, N. (2020). Technical trading rules in the cryptocurrency market. *Finance Research Letters*, 32, 101396. [Semantic Scholar](https://www.semanticscholar.org/paper/Technical-trading-rules-in-the-cryptocurrency-Grobys-Ahmed/2e9d6a7afbb88400c9b608ed752dfdb68f72cb90)
- Gurrib, I. (2018). Performance of the Average Directional Index as a market timing tool for the most actively traded USD based currency pairs. *Banks and Bank Systems*, 13(3), 58-70. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3232982)
- He, S., Manela, A., Ross, O., von Wachter, V. (2022). Fundamentals of Perpetual Futures. Working paper. [arXiv](https://arxiv.org/abs/2212.06888)
- Hudson, R., Urquhart, A. (2021). Technical trading and cryptocurrencies. *Annals of Operations Research*, 297, 191-220. [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)
- Hurst, B., Ooi, Y. H., Pedersen, L. H. (2017). A Century of Evidence on Trend-Following Investing. *Journal of Portfolio Management*, 44(1), 15-29. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026)
- Lee, C. M. C., Swaminathan, B. (2000). Price Momentum and Trading Volume. *Journal of Finance*, 55(5), 2017-2069. [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00280)
- Lento, C., Gradojevic, N., Wright, C. (2007). Investment information content in Bollinger Bands? *Applied Financial Economics Letters*, 3(4), 263-267.
- Liu, Y., Tsyvinski, A. (2021). Risks and Returns of Cryptocurrency. *Review of Financial Studies*, 34(6), 2689-2727. [NBER](https://www.nber.org/papers/w24877)
- Marshall, B. R., Cahan, R. H., Cahan, J. M. (2008). Does intraday technical analysis in the U.S. equity market have value? *Journal of Empirical Finance*, 15(2), 199-210. [EconPapers](https://econpapers.repec.org/RePEc:eee:empfin:v:15:y:2008:i:2:p:199-210)
- Moreira, A., Muir, T. (2017). Volatility-Managed Portfolios. *Journal of Finance*, 72(4), 1611-1644. [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12513)
- Moskowitz, T. J., Ooi, Y. H., Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics*, 104(2), 228-250. [PDF](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf)
- Park, C.-H., Irwin, S. H. (2007). What Do We Know About the Profitability of Technical Analysis? *Journal of Economic Surveys*, 21(4), 786-826. [EconPapers](https://econpapers.repec.org/article/blajecsur/v_3a21_3ay_3a2007_3ai_3a4_3ap_3a786-826.htm)
- Sullivan, R., Timmermann, A., White, H. (1999). Data-Snooping, Technical Trading Rule Performance, and the Bootstrap. *Journal of Finance*, 54(5), 1647-1691. [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00163)
- Tsang, W. W. H., Chong, T. T. L. (2009). Profitability of the On-Balance Volume Indicator. *Economics Bulletin*, 29(3), 2424-2431. [IDEAS](https://ideas.repec.org/a/ebl/ecbull/eb-09-00423.html)
- Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*. Trend Research. (Origine di RSI, SAR parabolico, ATR, ADX.)
