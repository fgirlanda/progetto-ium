# Diario lavori progetto Interfacce Uomo-Macchina

Autore: Girlanda Francesco

## Introduzione

Questo documento documenterà le attività svolte giorno per giorno al fine di replicare lo studio target selezionato*

*inserire riferimenti paper e dataset (licenza, url, ...)


## 5/06/2026

### Interpretazione dataset

- url non funzionante <http://subjectbook.times.uh.edu/>
- denominazione file fino a T088, ma numero verificato: 68
- la directory scaricata (R-Friendly Study Data) contiene i segnali in formato flat in un unica tabella (una per soggetto)
- ignorare dati di eyetracking aggiunti nella directory scaricata
- ignorare dati relativi alla guida (velocità, accelerazione ecc.)

### Ambiente di sviluppo

#### Progettazione

- linguaggio: `python 3.12.0`

##### Cosa serve

- gestione file csv: `pandas` v2.2
- manipolazione numerica: `numpy` (formato standard per librerie scientifiche) v2.2
- processing dei segnali: `scipy` v1.15
- visualizzazione segnali: `matplotlib` v3.10
- machine learning: `scikit-learn` v1.6
- salvataggio dati: `joblib` v1.5
- monitor progresso operazioni lunghe: `tqdm` v4.67

#### Setup

- installato python 3.12.0
- creato ambiente virtuale + requirements

#### Dataset

- setup pulizia dataset
  - ignorate colonne irrilevanti
  - ignorati soggetti con segnali mancanti (da 68 a 53)


## 6/06/2026

### Dataset

#### Interpretazione

- l'esperimento 1 ha 7 sezioni: B, PD, RD, LD, CD, ED, MD
- la sessione B viene scartata nel paper
- c'è una sessione extra (8) nei file csv scaricati: la scarto (?)
- stabilito che:
  - **sessione 8 scartata** 
  - media calcolata solo su valori validi e numero di valori validi (calcolo separato per ogni segnale)
  - se valori fuori range >= 30% totale elimino tutto il soggetto (?)

- **l'ordine delle sessioni da 4 a 7 è random (ma proprio random)**

#### Operazioni svolte

- metodo per generazione file csv intermedi per la verifica di ogni passaggio
- estratte misurazioni diverse per ogni soggetto
- ignorare soggetti con valori fuori range per un tempo > 30%
- assegnare media segnale a valori fuori range per un tempo <30%
- **compromesso: accettati 38 soggetti al posto di 37 post-pulizia**

### Features

- inizio feature extraction


## 7/06/2026

### Features

- divisione in segmenti in modo manuale (NON usando `rolling` perchè restituisce valori NaN che andrebbero gestiti aumentando la complessità)
- estrazione feature per ogni segmento usando `scipy` e `numpy`
- creazione lista_stree e lista_no_stress, ogni lista contiene tuple (che rappresentano i singoli segmenti) formate da:
  - id soggetto
  - tipo segnale
  - dict features
- trasformazione liste in dataframe (formato richiesto da `scikit-learn`)
- generazione csv `full_set`

