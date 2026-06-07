import os
from pathlib import Path
import numpy as np
import pandas as pd
from pandas import DataFrame
import scipy as sp
from scipy import stats as st

# parto da soggetti_in_range -> with os.scandir(soggetti_in_range)
# per ogni soggetto (cartella) -> for dir_soggetto in subdirs
    # estraggo id soggetto -> int(dir_soggetto.name[1:])
    # per ogni file (sessione) -> os.scandir(dir_soggetto)
        # lettura csv -> read_csv
        # tipo sessione (CD, PD, RD, ...) -> sessione.name (opportunamente processato)
        # per ogni segnale (colonna) -> df[["Time", "Tipo.Segnale"]] + dict segnali
            # estrarre segmento -> da tempo_corrente fino a min(tempo_corrente+60, tempo_totale)
            # calcolo le feature
            # passo al segmento successivo -> tempo_corrente += 30

# struttura dati esterna -> lista stress ()

    # struttura dati interna -> tupla

        # id soggetto -> int
        # tipo segnale (br, hr, peda, pereda)
        # segmenti (che contengono feature) -> tupla
        
# struttura dati esterna -> lista no -stress

    # struttura dati interna -> tupla

        # soggetto -> int
        # tipo segnale (br, hr, peda, pereda)
        # segmenti (che contengono feature) -> tupla

def main():
    path = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data\\soggetti_in_range'
    
    stress_sessions = ["CD", "ED", "MD"]

    lista_stress = []
    lista_no_stress = []
    
    with os.scandir(path) as subdirs:
        for dir_soggetto in subdirs:
            id_soggetto = int(dir_soggetto.name[1:])

            with os.scandir(dir_soggetto) as sessioni:
                for sessione in sessioni:
                    stress = ((Path(sessione.name)).stem.split("_")[1] in stress_sessions) # True = stress, Flase = no_stress
                    # lettura sessione
                    df = pd.read_csv(sessione)
                    
                    # estrazione segnali
                    segnale_peda = df[["Time", "Palm.EDA"]]
                    segnale_hr = df[["Time", "Heart.Rate"]]
                    segnale_br = df[["Time", "Breathing.Rate"]]
                    segnale_pereda = df[["Time", "Perinasal.Perspiration"]]
                    
                    segnali = {
                        "Palm.EDA": segnale_peda,
                        "Heart.Rate": segnale_hr,
                        "Breathing.Rate": segnale_br,
                        "Perinasal.Perspiration": segnale_pereda
                    }
                    
                    # estrazione feature su segmenti
                    for tipo_segnale, dati_segnale in segnali.items():
                        finestra = 60
                        step = 30 # overlap 50%
                        
                        t_inizio = df["Time"].min()
                        t_fine = df["Time"].max()
                        
                        t_corrente = t_inizio
                        t_fine_segmento = t_inizio
                        while(t_fine_segmento < t_fine):
                            # estraggo segmento
                            t_fine_segmento = min(t_corrente + finestra, t_fine) 
                            segmento = dati_segnale[(dati_segnale["Time"] >= t_corrente) & (dati_segnale["Time"] < t_fine_segmento)]
                            
                            
                            # calcolo features
                            features = extract_features(segmento)
                            
                            # salvare features segmento
                            if stress:
                                lista_stress.append((id_soggetto, tipo_segnale, features))
                            else:
                                lista_no_stress.append((id_soggetto, tipo_segnale, features))
                            
                            # passo a segmento successivo
                            t_corrente += step
                            
                            
    
    print(len(lista_stress))
    print(len(lista_no_stress))             

def extract_features(segmento: DataFrame):
    dati = segmento.iloc[:, 1]
    
    # (5) Standard deviation of the intensity values;                  
    std = dati.std()
    # (1) Arithmetic mean of the intensity values;
    arith_mean = dati.mean()  
    # (2) Median of the intensity values;                               
    median = dati.median()
    

    # (6) Variance of the intensity values;                                     
    variance = dati.var()
    if std < 1e-7:
        four_moment = five_moment = kurtosis = skew = np.nan                                  
    else:
        # (3) The fourth moment; 
        four_moment = st.moment(dati, moment=4)
        # (4) The fifth moment;    
        five_moment = st.moment(dati, moment=5)
        # (7) The fourth standard moment, also known as Kurtosis, of the intensity values;                                    
        kurtosis = st.kurtosis(dati)
        # (8) Skewness of the intensity values;                             
        skew = st.skew(dati)
        
    # (9) Sum of the intensity values;                                     
    sum = dati.sum()
    # (11) Maximum of the intensity values;                                         
    max = dati.max()
    # (12) Minimum of the intensity values;                                         
    min = dati.min()
    # (10) Range between maximum and minimum of the intensity values;                                         
    range = max - min  
    # (13) Root mean square error of the intensity values;                                      
    rms = np.sqrt(np.mean(dati**2))
    # (14) Entropy;                          
    entropy = st.entropy(np.histogram(dati, bins=10)[0] + 1)
    # (15) Interquartile range of the intensity values; 
    iqr = st.iqr(dati)                                       
    # (16) Spectral power density;
    freqs, spd = sp.signal.welch(dati, fs=1.0, nperseg=len(dati))
    # (17) Mean of the spectral power density;              
    spd_mean = np.mean(spd)
    # (18) Median of the spectral power density;                                  
    spd_median = np.median(spd)       
                          
    rmsd = intervals_std = np.nan
    peaks, _ = sp.signal.find_peaks(dati)
    if len(peaks) >= 2:
        intervals = np.diff(peaks)
    
        if len(peaks) >= 3:
            # (19) Root mean square of the differences between two successive peaks;
            rmsd = np.sqrt(np.mean(np.diff(intervals)**2))
        # (20) Standard deviation of the intervals between two successive peaks;           
        intervals_std = np.std(intervals)                      
    
    """
    il tempo è suddiviso in secondi, per cui è impossibile recuperare, da questa versione del dataset, una sensibilità nell'ordine dei ms
    la feature perderebbe di significato, quindi viene omessa
    
    n_diff_intervals = np.sum(np.abs(np.diff(intervals)) > 50)         # (21) The number of pairs of successive peaks intervals that differ by more than 50 ms.
    """
    features = {
        "arith_mean" : arith_mean,                                 
        "median" : median,                                   
        "four_moment" : four_moment,                
        "five_moment" : five_moment,                  
        "std" : std,                                         
        "variance" : variance,                                    
        "kurtosis" : kurtosis,                          
        "skew" : skew,                                      
        "sum" : sum,                                   
        "max" : max,                                   
        "min" : min,                                   
        "range" : range,                                   
        "rms" : rms,                       
        "entropy" : entropy,
        "iqr" : iqr,                                        
        "freqs" : freqs,              
        "spd_mean" : spd_mean,                                   
        "spd_median" : spd_median,                        
        "rmsd" : rmsd,           
        "intervals_std" : intervals_std,                     
    }
    
    return features

if __name__ == "__main__":
    main()