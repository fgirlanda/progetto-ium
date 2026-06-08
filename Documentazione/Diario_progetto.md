# Diario di Progetto – Replica Parziale di "Multimodal Car Driver Stress Recognition"

**Autore:** Francesco Girlanda

## Introduzione

Questo progetto nasce con l'obiettivo di replicare parzialmente il lavoro:

**Simone Bianco, Paolo Napoletano, Raimondo Schettini**
*Multimodal Car Driver Stress Recognition*
PervasiveHealth 2019.

L'articolo propone un sistema di riconoscimento dello stress del conducente basato su segnali fisiologici acquisiti durante sessioni di guida simulata. Il problema viene formulato come classificazione binaria tra condizioni di stress e non stress utilizzando diverse tecniche di machine learning.

La replica realizzata si concentra sulle fasi di:

* preprocessing del dataset;
* pulizia dei segnali;
* segmentazione temporale;
* estrazione delle feature;
* classificazione mediante k-Nearest Neighbors e Support Vector Machine.

Non sono state implementate le componenti più avanzate del paper, quali reti neurali artificiali, classificatori ensemble e fusione multimodale delle feature.

---

# 05/06/2026

## Analisi del dataset

Durante la fase iniziale è stato analizzato il dataset utilizzato nel paper.

Osservazioni principali:

* il link originale indicato dagli autori non risulta più disponibile;
* la versione scaricata contiene dati riformattati ("R-Friendly Study Data");
* i dati di eye-tracking non sono stati utilizzati;
* sono stati ignorati i dati relativi alla dinamica del veicolo (velocità, accelerazione, frenata, posizione corsia).

Sono stati mantenuti esclusivamente i segnali fisiologici:

* Palm EDA (P-EDA)
* Heart Rate (HR)
* Breathing Rate (BR)
* Perinasal Perspiration (PER-EDA)

## Ambiente di sviluppo

### Linguaggio

* Python 3.12

### Librerie utilizzate

| Libreria     | Utilizzo                               |
| ------------ | -------------------------------------- |
| pandas       | gestione file CSV                      |
| numpy        | elaborazione numerica                  |
| scipy        | signal processing e feature extraction |
| matplotlib   | visualizzazione dati                   |
| scikit-learn | classificazione                        |

## Pulizia preliminare

Sono state eliminate:

* colonne non pertinenti;
* registrazioni contenenti valori mancanti;
* soggetti che presentavano errori segnalati dalla colonna `Failure`.

Dopo questa prima fase il numero di soggetti disponibili è stato ridotto da 68 a 53.

---

# 06/06/2026

## Studio delle sessioni sperimentali

L'Esperimento I del paper è composto dalle seguenti sessioni:

* B (Baseline)
* PD (Practice Drive)
* RD (Relaxing Drive)
* LD (Loaded Drive)
* CD (Cognitive Drive)
* ED (Emotional Drive)
* MD (Motor Drive)

La sessione Baseline viene esclusa come indicato nell'articolo.

Nella versione del dataset utilizzata è presente inoltre una sessione aggiuntiva (identificata come sessione 8), che è stata rimossa.

## Assunzioni adottate

Durante l'analisi è emersa una differenza rispetto alla struttura descritta nel paper.

Nel dataset originale le sessioni da LD a MD risultano randomizzate tra i soggetti.

Nella versione R-Friendly tale informazione non è disponibile in maniera esplicita. Per questo motivo è stata adottata la seguente corrispondenza:

| Sessione | Etichetta |
| -------- | --------- |
| 2        | PD        |
| 3        | RD        |
| 4        | LD        |
| 5        | CD        |
| 6        | ED        |
| 7        | MD        |

## Gestione dei valori fuori range

Sono state implementate le stesse soglie riportate nell'articolo:

| Segnale        | Range valido |
| -------------- | ------------ |
| Heart Rate     | 40 – 120     |
| Breathing Rate | 4 – 40       |
| Palm EDA       | 28 – 628     |

Per ogni sessione:

* se oltre il 30% dei campioni risultava fuori range, la sessione veniva eliminata;
* altrimenti i valori anomali venivano sostituiti con la media dei campioni validi dello stesso segnale.

Al termine della procedura sono stati mantenuti 33 soggetti.

---

# 07/06/2026

## Segmentazione temporale

I segnali sono stati segmentati manualmente utilizzando:

* finestra di 60 secondi;
* overlap del 50%;
* avanzamento di 30 secondi.

Questa configurazione replica quella utilizzata nel paper.

## Estrazione delle feature

Per ciascun segmento sono state estratte 20 feature.

Le feature comprendono:

### Dominio del tempo

* media
* mediana
* quarto momento
* quinto momento
* deviazione standard
* varianza
* kurtosis
* skewness
* somma
* massimo
* minimo
* range
* RMS
* entropia
* IQR

### Dominio della frequenza

* spectral power density
* media PSD
* mediana PSD

### Feature basate sui picchi

* RMS delle differenze tra intervalli
* deviazione standard degli intervalli

Le feature sono state organizzate in un dataset tabellare utilizzabile da scikit-learn.

## Gestione dei valori mancanti

Per segmenti con varianza quasi nulla non è stato possibile calcolare:

* quarto momento;
* quinto momento;
* kurtosis;
* skewness.

Tali valori sono stati marcati come NaN.

---
# 08/06/2026

## Pulizia finale delle feature

Le osservazioni contenenti NaN nelle feature:

* four_moment
* five_moment
* kurtosis
* skew

sono state eliminate.

I NaN presenti nelle feature:

* rmsd
* intervals_std

sono stati sostituiti mediante imputazione della media.

## Classificazione

Sono stati implementati due classificatori:

### k-Nearest Neighbors

Configurazione:

* k = 1
* distanza euclidea

### Support Vector Machine

Configurazione:

* kernel RBF
* parametri di default di scikit-learn

## Validazione

È stata utilizzata:

* Stratified 5-Fold Cross Validation

Prima dell'addestramento è stata applicata una normalizzazione Min-Max calcolata esclusivamente sul training set di ciascun fold.

## Risultati

Le accuratezze ottenute risultano comparabili con quelle riportate nel paper per i segnali considerati singolarmente.

I risultati mostrano una buona coerenza generale nonostante le differenze presenti tra il dataset utilizzato e quello originale.



