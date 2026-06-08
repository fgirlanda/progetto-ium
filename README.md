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
├── step1_preprocessing.py
├── step2_feature_extraction.py
├── step3_classification.py
│
└── data/
    ├── soggetti/
    ├── soggetti_in_range/
    ├── full_set/
    └── results/
```

## Pipeline (comandi lanciati all'interno della directory del progetto)

### Step 1 – Preprocessing

Operazioni:

* eliminazione colonne non necessarie;
* rimozione soggetti con dati mancanti;
* eliminazione sessioni non valide;
* sostituzione valori fuori range;
* esportazione dataset intermedi.

Esecuzione:

```bash
python src/dataset/pulizia_dataset.py
```

Output:

```text
data/soggetti/
data/soggetti_in_range/
```

---

### Step 2 – Feature Extraction

Operazioni:

* segmentazione 60 s;
* overlap 50%;
* estrazione di 20 feature statistiche e spettrali;
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
python src/classification/classification.py
```

Output:

```text
data/full_set/full_set_clean.csv
data/results/results.csv
```

## Risultati

I risultati ottenuti sono confrontabili con quelli riportati nel paper per la classificazione dei singoli segnali fisiologici.

Esempio:

| Segnale | kNN Paper | kNN Replica | SVM Paper | SVM Replica |
| ------- | --------- | ----------- | --------- | ----------- |
| PEDA    | 53.88%    | 51.15%      | 54.31%    | 56.37%      |
| HR      | 58.72%    | 50.43%      | 56.87%    | 56.09%      |
| BR      | 55.97%    | 53.58%      | 62.39%    | 63.00%      |
| PEREDA  | 54.54%    | 53.65%      | 61.42%    | 58.91%      |

## Limitazioni

Questa replica non implementa:

* Artificial Neural Networks (ANN);
* Stacking classifier;
* Fusione multimodale delle feature;
* Leave-One-Subject-Out Cross Validation;
* Ricerca automatica degli iperparametri SVM.

## Autore

Francesco Girlanda

## Licenza

Progetto sviluppato esclusivamente per finalità didattiche e di ricerca universitaria.
