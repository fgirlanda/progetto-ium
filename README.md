# Multimodal Driver Stress Recognition (Partial Replication)

Replica parziale del paper:

> Bianco S., Napoletano P., Schettini R.
> *Multimodal Car Driver Stress Recognition*
> PervasiveHealth 2019

## Obiettivo

L'obiettivo del progetto è replicare parte della pipeline proposta dagli autori, al fine di ottenere dei risultati sufficientemente simili e coerenti con le semplificazioni adottate.

Il progetto include:

* preprocessing del dataset;
* pulizia dei segnali;
* segmentazione temporale;
* estrazione delle feature;
* classificazione tramite kNN e SVM.

## Dataset

Il progetto utilizza la versione riformattata del dataset:

**R-Friendly Study Data**

Segnali utilizzati:

* Palm EDA
* Heart Rate
* Breathing Rate
* Perinasal Perspiration

Segnali ignorati:

* Eye Tracking
* Telemetrie di guida
* Altri segnali non utilizzati dal paper

## Requisiti

### Python

```bash
Python >= 3.12
```

### Dipendenze

```bash
pip install pandas numpy scipy matplotlib scikit-learn joblib tqdm
```

oppure

```bash
pip install -r requirements.txt
```

## Struttura del progetto

```text
src/
│
├── dataset/
|   ├── pulizia_dataset.py
|   └── feature_extraction.py
├── classification/
|   └── classify.py
├── utility/
|   └── utility.py
│
└── data/
    ├── deleted_missing/
    ├── full_set/
    ├── results/
    ├── soggetti/
    ├── soggetti_in_range/
    └── without_car_data/
```

## Pipeline (comandi lanciati all'interno della directory del progetto)

### Step 1 – Preprocessing

Operazioni:

1. eliminazione colonne non necessarie;
2. rimozione soggetti con dati mancanti;
3. a) eliminazione sessioni non valide;
3. b) sostituzione valori fuori range;
4. esportazione dataset intermedi.

Esecuzione:

```bash
python -m src.dataset.pulizia_dataset
```

Output:

```text
1. data/without_car_data/
2. data/deleted_missing/
3.a data/soggetti/
3.b data/soggetti/
4. data/soggetti_in_range/
```

---

### Step 2 – Feature Extraction

Operazioni:

* segmentazione 60 s;
* overlap 50%;
* estrazione di 20 feature;
* generazione dataset finale.

Esecuzione:

```bash
python -m src.dataset.feature_extraction
```

Output:

```text
data/full_set/full_set.csv
```

---

### Step 3 – Classification

Operazioni:

* gestione NaN;
* normalizzazione Min-Max;
* classificazione kNN;
* classificazione SVM;
* validazione Stratified 5-Fold.

Esecuzione:

```bash
python -m src.classification.classify
```

Output:

```text
data/full_set/full_set_clean.csv
data/results/results.csv
```

## Risultati

I risultati ottenuti sono confrontabili con quelli riportati nel paper per la classificazione dei singoli segnali fisiologici:

| Segnale | kNN Paper | kNN Replica | SVM Paper | SVM Replica |
| ------- | --------- | ----------- | --------- | ----------- |
| PEDA    | 53.88%    | 51.17%      | 54.31%    | 56.45%      |
| HR      | 58.72%    | 50.22%      | 56.87%    | 56.09%      |
| BR      | 55.97%    | 53.80%      | 62.39%    | 62.55%      |
| PEREDA  | 54.54%    | 53.78%      | 61.42%    | 59.12%      |

Mentre per quanto riguarda l'utilizzo di tutti i segnali, concatenando le feature, i risultati replicati si discostano parecchio da quelli originali:


Primo tentativo:

| Segnale | kNN Paper | kNN Replica | SVM Paper | SVM Replica |
| ------- | --------- | ----------- | --------- | ----------- |
| ALL     | 74.51%    | 53.62%      | 74.37%    | 61.40%      |

Secondo tentativo:

| Segnale | kNN Paper | kNN Replica | SVM Paper | SVM Replica |
| ------- | --------- | ----------- | --------- | ----------- |
| ALL     | 74.51%    | 88.00%      | 74.37%    | 99.9%       |

Terzo tentativo:

| Segnale | kNN Paper | kNN Replica | SVM Paper | SVM Replica |
| ------- | --------- | ----------- | --------- | ----------- |
| ALL     | 74.51%    | 83.50%      | 74.37%    | 99.8%       |


Questa replica non implementa:

* Artificial Neural Networks (ANN);
* Stacking classifier;
* Ricerca automatica degli iperparametri SVM.

## Semplificazioni introdotte

### Riduzione del numero di feature

Il paper utilizza 21 feature.

La replica utilizza 20 feature.

La feature:

> numero di coppie di intervalli tra picchi che differiscono di oltre 50 ms

è stata omessa poiché il dataset disponibile non consente misurazioni con precisione nell'ordine dei millisecondi.

### Dataset differente

È stata utilizzata la versione "R-Friendly Study Data" invece del dataset originale.

### Numero di soggetti

* Paper: 37 soggetti
* Replica: 33 soggetti

### Classificatori non implementati

Non sono stati implementati:

* Stacking classifier.

---

# Conclusioni

La replica realizzata riproduce correttamente le principali fasi di preprocessing, segmentazione ed estrazione delle feature descritte nell'articolo.

I risultati ottenuti risultano coerenti con le semplificazioni metodologiche e l'utilizzo di una diversa versione del dataset, c'è un margine relativamente piccolo di errore rispetto a quelli pubblicati dagli autori per i singoli segnali fisiologici, mentre il margine aumenta per quanto riguarda la concatenazione delle feature. 

Primo tentativo: non tenere traccia dell'id del segmento e della sessione, durante l'estrazione delle feature, ha causato valori NaN che sono stati poi eliminati, portando a un disallineamento delle finestre e deteriorando le performance del modello.

Secondo tentativo: le finestre sono allineate, ma probabilmente il data leakage, dovuto all'imputazione operata su tutto il dataset per valori NaN, non è più trascurabile, dato che concatenare ha aumentato lo spazio delle feature 

Terzo tentativo: l'imputazione è stata spostata dentro al singolo fold, tuttavia i risultati sono comunque errati, le cause possono essere il numero minore di soggetti post-pulizia (33 vs 37), la 21esima feature non utilizzata o un passaggio errato nell'estrazione delle feature


## Autore

Francesco Girlanda

## Licenza

Progetto sviluppato esclusivamente per finalità didattiche e di ricerca universitaria.
