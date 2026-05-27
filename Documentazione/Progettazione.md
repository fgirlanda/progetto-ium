# Fase preparatoria del progetto

## Dataset scelto: physio_driving
*A dataset on the physiological state and behavior of drivers 
in conditionally automated driving* — Meteier et al., 2023

### Caratteristiche
- 346 soggetti, 6 esperimenti distinti
- Segnali raccolti: ECG, EDA, RESP
- Frequenza di campionamento: 1000 Hz
- Accesso: pubblico su Zenodo (DOI: 10.5281/zenodo.7214953), 
  licenza CC BY 4.0
- Feature fisiologiche pre-calcolate disponibili (NeuroKit2)

### Esperimento selezionato
> ⚠️ Da definire: candidati principali sono **Exp4** 
> (fatica/sleep deprivation, label binaria alert vs. drowsy) 
> e **Exp2/Exp3** (carico cognitivo a 2/3 livelli).
> La scelta influenza il task di classificazione e 
> la compatibilità con lo studio target.

---

## Studio target: Bianco et al., 2019
*Multimodal Car Driver Stress Recognition*

### Caratteristiche
- Task: classificazione binaria **stress vs. no-stress**
- Dataset originale: Taamneh et al., 2017 (simulatore di guida)
- Segnali usati: HR, BR, P-EDA, PER-EDA
- Soggetti dopo pulizia: 37 (su 68 iniziali)
- Miglior accuratezza: 77.25% (5-fold), 65.09% (leave-one-out)

---

## Considerazioni sul mapping dei segnali

| Segnale (Bianco) | Segnale (physio_driving) | Note |
|---|---|---|
| HR | ECG | Estraibile tramite rilevamento picchi R |
| BR | RESP | Compatibile |
| P-EDA | EDA | Compatibile |
| PER-EDA | ❌ Non disponibile | Estratta da video termico periasale — assente nel dataset Meteier |

L'assenza di PER-EDA è rilevante: nel paper originale è il secondo 
segnale più discriminativo dopo BR. Il suo impatto sulle performance 
sarà uno degli elementi da analizzare nel confronto cross-dataset.

Ulteriore differenza di contesto: Bianco usa dati di **guida manuale** 
con stressor indotti, mentre physio_driving è prevalentemente 
**guida automatizzata (L3)**. Questo può influenzare la natura 
dell'attivazione fisiologica e quindi le performance del modello.

---

## Replica dello studio target

### Pre-processing

#### Pulizia del segnale
Criteri di validità per intervallo:

| Segnale | Intervallo valido |
|---|---|
| HR | [40, 120] bpm |
| BR | [4, 40] bpm |
| P-EDA | [28, 628] kΩ |

Regole di applicazione:
- Valori fuori intervallo per **≥ 30%** della durata del record → 
  record rimosso
- Valori fuori intervallo per **< 30%** della durata → 
  sostituiti con la media del record
- Valori mancanti in uno qualsiasi dei 4 segnali → record rimosso

*Risultato atteso sul dataset originale: 68 → 37 soggetti*

#### Segmentazione
- Dimensione finestra: **W = 60 s**
- Overlap: **L = 50%**

*Nel paper originale sono stati testati W ∈ [50, 400] s 
e L ∈ [25%, 75%]. I valori scelti sono quelli ottimali 
riportati dagli autori.*

---

### Feature extraction

Per ogni finestra e per ogni segnale vengono estratte 
le seguenti **21 feature**:

**Time-domain:**
1. Media aritmetica
2. Mediana
3. Quarto momento
4. Quinto momento
5. Deviazione standard
6. Varianza
7. Curtosi (quarto momento standardizzato)
8. Skewness
9. Somma
10. Range (max - min)
11. Massimo
12. Minimo
13. Root Mean Square (RMS)
14. Entropia
15. Interquartile Range (IQR)

**Frequency-domain:**

16. Densità spettrale di potenza (PSD)
17. Media della PSD
18. Mediana della PSD

**Peak-based:**

19. RMSSD — Root Mean Square delle differenze 
    tra picchi successivi
20. SDNN — Deviazione standard degli intervalli 
    tra picchi successivi
21. pNN50 — Numero di coppie di picchi successivi 
    con differenza > 50 ms

> ⚠️ Le feature 3 e 4 ("fourth moment" e "fifth moment") 
> non sono esplicitate con formula nel paper. 
> Verificare se si intendono momenti centrali o standardizzati 
> prima dell'implementazione.

#### Normalizzazione
- **Training set**: ogni feature normalizzata nell'intervallo [0, 1]
- **Test set**: normalizzato usando i parametri (min, max) 
  calcolati sul training set

---

### Classificazione

**Classi target:**
- 🔴 stress
- 🟢 no-stress

| Condizione | Classe | Descrizione |
|---|---|---|
| CD — Cognitive Drive | 🔴 stress | Stressore cognitivo: domande matematiche |
| ED — Emotional Drive | 🔴 stress | Stressore emotivo: domande coinvolgenti |
| MD — Sensorimotor Drive | 🔴 stress | Stressore sensomotorio: risposta a SMS |
| PD — Practice Drive | 🟢 no-stress | Familiarizzazione col simulatore |
| RD — Relaxing Drive | 🟢 no-stress | Guida rilassante con istruzioni |
| LD — Loaded Drive | 🟢 no-stress | Guida senza stressor aggiuntivi |

*Durata sessioni: PD e RD ~500 s; LD, CD, ED e MD ~800 s*

**Classificatori da implementare** (come nel paper originale):
- k-NN (k=1, distanza euclidea)
- SVM (kernel RBF, grid search su C e γ)
- ANN (shallow autoencoder + softmax)
- STACK (majority vote dei tre classificatori)

**Setup di validazione:**
- 5-fold cross-validation stratificata
- Leave-one-subject-out (più sfidante, testa la generalizzazione)

**Metriche di valutazione:**
- Micro accuracy (gestisce lo sbilanciamento delle classi)
- Accuracy per classe separata (stress vs. no-stress)
- Precision, Recall, F1-score

---

## TODO

### Fase 0 — Preparazione
- [ ] Revisione approfondita dei paper analizzati, 
      con focus sulla pipeline di Bianco et al.
- [ ] Setup ambiente di sviluppo 
      (Python consigliato per disponibilità librerie: 
      MNE, NeuroKit2, scikit-learn)
- [ ] Download del dataset physio_driving da Zenodo
- [ ] Scelta definitiva dell'esperimento del dataset 
      da utilizzare (Exp4 vs Exp2/Exp3)

### Fase 1 — Replica dello studio target
- [ ] Implementazione del pre-processing 
      (pulizia, segmentazione)
- [ ] Implementazione della feature extraction (21 feature)
- [ ] Implementazione e confronto dei classificatori 
      (k-NN, SVM, ANN, STACK)
- [ ] Validazione: 5-fold cross-validation + 
      leave-one-subject-out
- [ ] Verifica dei risultati: confronto con quelli 
      riportati nel paper originale
- [ ] Analisi delle discrepanze (se presenti)

### Fase 2 — Applicazione cross-dataset
- [ ] Adattamento del pre-processing al dataset physio_driving
      (gestione PER-EDA mancante, diversa fs, 
      diverso tipo di label)
- [ ] Definizione delle label per il task binario 
      sul nuovo dataset
- [ ] Esecuzione della pipeline sul nuovo dataset
- [ ] Confronto dei risultati con Fase 1

### Fase 3 — Analisi critica e conclusioni
- [ ] Analisi dell'impatto dell'assenza di PER-EDA 
      sulle performance
- [ ] Analisi del contributo dei singoli segnali 
      (ablation study: singolo segnale vs. tutti)
- [ ] Confronto tra 5-fold e leave-one-subject-out: 
      quanto cala la generalizzazione?
- [ ] Redazione della presentazione