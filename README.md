Link clone repository: https://github.com/iCon-just-order-team/just-order.git

# Membri del gruppo:
- Borraccino Carmela, matricola: 706420, email: c.borraccino3@studenti.uniba.it
- Brescia Davide, matricola: 698377, email: d.brescia3@studenti.uniba.it
- Cioce Giuseppe, matricola: 700015, email: g.cioce4@studenti.uniba.it

# Introduzione al progetto
Questo progetto nasce per agevolare i ristoratori nella gestione dell'inventario, nell'acquisto di alimenti e nel filtrare
i piatti in base a particolari scelte alimentari o intolleranze. 

Questo programma è strutturato principalmente in due parti:
una knowledge base che effettua un approfondimento sugli ingredienti presenti nei piatti e da una rete bayesiana in grado di predire l'affluenza.

## Casi D'uso
- `previsione_affluenza` - prevede l'affluenza nel locale, restituendo una percentuale che dipende da vari fattori approfonditi
 nella sezione dedicata alla Rete Bayesiana
- `inventario` - comunica gli ingredienti presenti nell'inventario
- `ho_acquistato INGREDIENTE QTY` - aggiorna l'inventario aggiungendo un numero QTY all'ingrediente INGREDIENTE. La quantità di default è 1.
- `cucina PIATTO` - cucina il PIATTO inserito, modificando il numero di alimenti presenti nell'inventario
- `menu` - mostra il menu a disposizione
- `cerca_ingrediente INGREDIENTE1 INGREDIENTE2 ...` - mostra tutti i piatti che contengono questi INGREDIENTI (and logico)
- `piatto_disponibile PIATTO` - dice se, in base agli ingredienti nell'inventario, e' possibile servire il PIATTO
- `caratteristica_piatto INTOLLERANZA/SCELTA-ALIMENTARE PIATTO` - considerando l'INTOLLERANZA o la SCELTA ALIMENTARE 
  comunica se si può mangiare il PIATTO
- `query QUERY` - permette di effettuare una query al kb
- `exit` - esce dal programma

## Guida all'installazione
- *pyswip* - libreria per implementare prolog swish
  Installazione tramite `pip install pyswip`
- *pybbn* - libreria per l'implementazione di una rete bayesiana
  Installazione tramite `pip install pybbn`
- Installazione *Swi-Prolog*, tramite il sito web - https://www.swi-prolog.org/

## Scelte progettuali
- **Rete Bayesiana**: abbiamo scelto una rete bayesiana a causa dell'incertezza data da diversi fattori. Grazie alla rete bayesiana
è possibile anche ignorare alcune caratteristiche per ottenere una stima più generale. Per esempio possiamo scegliere di prevedere
  se in una settimana (rispondendo "non so" alla domanda "E' un giorno del weekend"), in base a diverse caratteristiche il
  locale si andrà a riempire o meno.
- **Rappresentazione Individuo-Proprietà-Valore**: abbiamo scelto questa caratteristica sia per avere una kb più ordinata e
sia per rispondere alla domanda in cui un concetto debba essere considerato come predicato o individuo. Tramite questa rappresentazione
  siamo giunti anche ad ottenere una rapprentazione grafica riportata in basso.
- **Uso delle classi**: dato che alcune categorie di ingredienti avevano qualcosa in comune (es. i risotti devono contenere
  sia riso che burro) sono state scelte le classi. L'utente quindi non dovrà inserire il riso e il burro qualora inserisca
  un piatto che fa parte della categoria risotto.

## Knowledge Base 
Nel nostro progetto abbiamo utilizzato il Prolog, che è un linguaggio di programmazione logica. 
Utilizza le assunzioni: CWA (closed word assumption) e UNA (unique name assumption).
Il sistema sarà dotato di una knowledge base che approfondirà due concetti principali:
- la gestione dell'inventario 
- filtro delle ricette.
  
La gestione dell'inventario servirà a tener traccia dei prodotti, l'utente potrà aggiungere alimenti 
e potrà anche cucinare piatti, rimuovendo quindi elementi dal magazzino.

Per quanto riguarda il filtraggio dei piatti, abbiamo strutturato la knowledge base sotto forma di
albero anche grazie all'utilizzo di **Individuo-Proprietà-Valore** e l'utilizzo delle **classi**.

Grazie alla struttura ad albero presente nella KB, sarà possibile visualizzare il menu in cui sono presenti tutte le ricette con gli ingredienti e si potrà visualizzare quale piatto è adatto ad una scelta alimentare o intolleranza.

![image](https://github.com/iCon-just-order-team/just-order/blob/main/grafo%20kb.png)

## Rete Bayesiana
E' stata prevista una feature che è in grado di predire l'affluenza di clienti al locale.
Il valore restituito dal comando sarà compreso tra 0 e 1: per valori che tendono ad 1 è stimata un'affluenza massima,
mentre per valori che tendono a 0 il sistema avrà previsto un'affluenza minima.

L'affluenza dipende da: fattori meteo, temperatura, giorno del weekend, periodo turistico, intrattenimento, qualità del cibo e competenza dello staff.
Sono state fatte diverse semplificazioni per trattare in modo più agevole il problema. Il grafo sotto riportato indica 
come è stata organizzata la dipendenza tra questi fattori.

![image](https://github.com/iCon-just-order-team/just-order/blob/main/Rete%20bayesiana.png)

**Meteo:** si è ipotizzata una località solitamente soleggiata che potrebbe essere del sud italia

| P(Meteo = Soleggiato) | P(Meteo = Nuvoloso) | P(Meteo = Pioggia) |
|-----------------------|---------------------|--------------------|
| 0.48                  | 0.31                | 0.21               |

**Temperatura:** Si è ipotizziato una città che ha temperature medie alte, 
anche qui si può considerare una città del sud italia

| P(Temperatura = Caldo) | P(Temperatura = Mite) | P(Temperatura = Freddo) |
|------------------------|-----------------------|-------------------------|
| 0.45                   | 0.43                  | 0.12                    |

**Fattore Climatico:**

| Meteo   | Temperatura | P(Fattore Climatico = buono) | P(Fattore Climatico = pessimo) |
|---------|-------------|------------------------------|--------------------------------|
| Sole    | Caldo       | 0.79                         | 0.21                           |
| Sole    | Mite        | 0.95                         | 0.05                           |
| Sole    | Freddo      | 0.45                         | 0.55                           |
| Nuvole  | Caldo       | 0.81                         | 0.19                           |
| Nuvole  | Mite        | 0.91                         | 0.09                           |
| Nuvole  | Freddo      | 0.32                         | 0.68                           |
| Pioggia | Caldo       | 0.12                         | 0.88                           |
| Pioggia | Mite        | 0.05                         | 0.95                           |
| Pioggia | Freddo      | 0.03                         | 0.97                           |

**Weekend:** indica la probabilità di essere nel weekend 2/7, 5/7 nel caso contrario

**Periodo Turistico:** Si è supposto che la cittadina abbia 2 mesi turistici principalmente quindi 2/12 nel caso positivo
e 10/12 nel caso negativo.

**Fattore Temporale:**

| Weekend | Periodo turistico | P(Fattore Temporale = buono) | P(Fattore Temporale = pessimo) |
|---------|-------------------|------------------------------|--------------------------------|
| Si      | Si                | 0.98                         | 0.02                           |
| Si      | No                | 0.65                         | 0.35                           |
| No      | Si                | 0.82                         | 0.18                           |
| No      | No                | 0.21                         | 0.79                           |


**Fattore Esterno:**

| Fattore Climatico | Fattore Temporale | P(Fattore Esterno = buono) | P(Fattore Esterno = pessimo) |
|-------------------|-------------------|----------------------------|------------------------------|
| Buono             | Buono             | 0.97                       | 0.03                         |
| Buono             | Pessimo           | 0.56                       | 0.44                         |
| Pessimo           | Buono             | 0.11                       | 0.89                         |
| Pessimo           | Pessimo           | 0.02                       | 0.98                         |

**Intrattenimento:** si è ipotizzato che il locale abbia un televisore e trasmetta eventi importanti 
ma faccia poche serate speciali

| P(Intrattenimento = Trasmissione evento) | P(Intrattenimento = Serata) | P(Intrattenimento = Nessuno) |
|------------------------------------------|-----------------------------|------------------------------|
| 0.15                                      | 0.04                        | 0.81                         |

**Qualità del cibo:** abbiamo ipotizzato che 8/10 piatti sono buoni

**Competenza dello staff:** abbiamo ipotizzato che 7/10 lo staff fa la cosa giusta

**Caratteristiche ristorante:**

| Qualità cibo | Competenza Staff | P(Caratteristiche Ristorante = Buono) | P(Caratteristiche Ristorante = Pessimo) |
|--------------|------------------|---------------------------------------|-----------------------------------------|
| Buono        | Buono            | 0.95                                  | 0.05                                    |
| Buono        | Pessimo          | 0.31                                  | 0.69                                    |
| Pessimo      | Buono            | 0.17                                  | 0.83                                    |
| Pessimo      | Pessimo          | 0.01                                  | 0.99                                    |

**Fattori Interni:**

| Intrattenimento | Caratteristiche Ristornate | P(Fattore Interno = Buono) | P(Fattore Interno = Pessimo) |
|-----------------|----------------------------|----------------------------|------------------------------|
| Trasmissione    | Buono                      | 0.97                       | 0.03                         |
| Trasmissione    | Pessimo                    | 0.45                       | 0.55                         |
| Serata          | Buono                      | 0.9                        | 0.1                          |
| Serata          | Pessimo                    | 0.13                       | 0.87                         |
| Nessuno         | Buono                      | 0.83                       | 0.17                         |
| Nessuno         | Pessimo                    | 0.06                       | 0.94                         |

**Probabilità di riempire il ristorante:**

| Fattori Interni | Fattori Esterni | P(Riempimento = Massimo) | P(Riempimento = Minimo) |
|-----------------|-----------------|--------------------------|-------------------------|
| Buono           | Buono           | 0.95                     | 0.05                    |
| Buono           | Pessimo         | 0.3                      | 0.7                     |
| Pessimo         | Buono           | 0.42                     | 0.58                    |
| Pessimo         | Pessimo         | 0.01                     | 0.99                    |

## Possibili espansioni:
-  Stima delle calorie dei piatti, utile per chi vuole tenere traccia delle calorie giornaliere.
-  Categorizzare le ricette come antipasto, primo, secondo ecc... Questo potrebbe essere utile per mostrare un menu più organizzato.
- Gestione del personale: ogni cameriere si dovrà occupare tutt'al più N tavoli, altrimenti i clienti dovranno aspettare molto tempo.
- Consiglio sugli acquisti alimentari giornalieri in base ad un dataset (in base a giorno della settimana, se è festivo o meno, se è soleggiato o meno,
  se si tratta di un periodo turistico, in base all'intrattenimento, in base alla qualità del cibo e dello staff).
- Consiglio sul numero di staff da contattare per un determinato giorno della settimana (in base alle cose sopracitate).
- Calcolare il percorso migliore per consegnare pietanze ai clienti che fanno richiesta d'asporto.

