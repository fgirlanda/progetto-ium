# Multimodal Driver Stress Recognition (Partial Replication)

Replica parziale del paper:

> Bianco S., Napoletano P., Schettini R.
> *Multimodal Car Driver Stress Recognition*
> PervasiveHealth 2019

## Obiettivo

L'obiettivo del progetto è replicare parte della pipeline proposta dagli autori per il riconoscimento automatico dello stress del conducente tramite segnali fisiologici.

La replica include:

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
python src/dataset/pulizia_dataset.py
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
python src/dataset/feature_extraction.py
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
python src/classification/classify.py
```

Output:

```text
data/full_set/full_set_clean.csv
data/results/results.csv
```

## Risultati

I risultati ottenuti sono confrontabili con quelli riportati nel paper per la classificazione dei singoli segnali fisiologici.

| Segnale | kNN Paper | kNN Replica | SVM Paper | SVM Replica |
| ------- | --------- | ----------- | --------- | ----------- |
| PEDA    | 53.88%    | 51.15%      | 54.31%    | 56.37%      |
| HR      | 58.72%    | 50.43%      | 56.87%    | 56.09%      |
| BR      | 55.97%    | 53.58%      | 62.39%    | 63.00%      |
| PEREDA  | 54.54%    | 53.65%      | 61.42%    | 58.91%      |

Questa replica non implementa:

* Artificial Neural Networks (ANN);
* Stacking classifier;
* Fusione multimodale delle feature;
* Leave-One-Subject-Out Cross Validation;
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

* Artificial Neural Networks (ANN);
* Stacking classifier.

### Fusione multimodale

Il paper valuta anche la concatenazione delle feature provenienti da tutti i segnali.

Nella replica ogni segnale è stato classificato separatamente.

### Leave-One-Subject-Out

Il protocollo LOSO presente nel paper non è stato implementato.

---

# Conclusioni

La replica realizzata riproduce correttamente le principali fasi di preprocessing, segmentazione ed estrazione delle feature descritte nell'articolo.

I risultati ottenuti risultano coerenti con le semplificazioni metodologiche e l'utilizzo di una diversa versione del dataset, c'è un margine relativamente piccolo di errore rispetto a quelli pubblicati dagli autori per i singoli segnali fisiologici.


## Autore

Francesco Girlanda

## Licenza

Progetto sviluppato esclusivamente per finalità didattiche e di ricerca universitaria.
