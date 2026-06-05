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
- setup pulizia dataset
  - ignorate colonne irrilevanti
  - ignorati soggetti con segnali mancanti