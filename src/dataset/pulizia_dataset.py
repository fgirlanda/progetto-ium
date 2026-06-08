import math
from pathlib import Path

import pandas as pd
import os

from src.utility.utility import generate_csv

############################################################
# TODO
# multi-thread
############################################################

def main():
    origin = r'C:\\DEV\\MATLAB\\progetto-ium\\Risorse\\R-Friendly Study Data'
    output_dir = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data'
    dataframes = []
    # B, PD, RD, LD, CD, ED, MD
    sections = {
        # 1: "B",
        2: "PD",
        3: "RD",
        4: "LD",
        5: "CD",
        6: "ED",
        7: "MD"
        # 8: "FDN/FDL/..."
    }
    
    
    with os.scandir(origin) as files:
        for file in files:
            df = extract_cols(file)
            generate_csv(df, output_dir + "\\without_car_data", Path(file.name).stem+"no_car") # csv senza colonne irrilevanti
            if not check_missing_signals(df):
                dataframes.append((Path(file.name).stem, df))

    
    for name, dataframe in dataframes:
        generate_csv(dataframe, output_dir + "\\deleted_missing", name+"data_exists") # csv senza soggetti con segnali mancanti
    
    for name, dataframe in dataframes:
        misurazioni = extract_measures(dataframe)
        for _, mis in enumerate(misurazioni):
            drive = mis["Drive"].iloc[0]
            drive = math.floor(drive)    
            generate_csv(mis, output_dir + f"\\soggetti\\{name}", name+f"sez_{sections[drive]}") # crea un csv per ogni sessione con label
            if not (out_of_range(mis)):
                generate_csv(mis, output_dir + f"\\soggetti_in_range\\{name}", name+f"sez_{sections[drive]}") # crea un csv per ogni sessione con label

                
# NON legge colonne non relative a segnali di interesse
def extract_cols(file):
    cols = ["Time", "Drive", "Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate", "Perinasal.Perspiration"]
    df = pd.read_csv(file, usecols=cols)
    return df[(df["Drive"] > 1) & (df["Drive"] < 8)]



# scarta soggetti che non presentano uno dei segnali richiesti in nessun istante di tempo
def check_missing_signals(df):
    signals_cols = ["Palm.EDA", "Heart.Rate", "Breathing.Rate", "Perinasal.Perspiration"]
    if df[signals_cols].isnull().any().any() or df[df["Failure"] > 0].any().any(): 
        return True
    else:
        return False
    



# estrae singole misurazioni per ogni soggetto
def extract_measures(df):
    misurazioni = []
    corrente = []

    for _, row in df.iterrows():
        if row["Time"] == 1 and corrente:
            # if not check_missing_signals(pd.DataFrame(corrente)): # non aggiungo sezioni con segnali mancanti
            misurazioni.append(pd.DataFrame(corrente))
            corrente = []
        corrente.append(row)  # fuori dall'if: la riga con Time==1 va nella nuova sessione

    if corrente:  # aggiungi l'ultima sessione
        misurazioni.append(pd.DataFrame(corrente))

    return misurazioni

# elaborazione sezioni con segnali fuori range
def out_of_range(df):
    # calcolare 30% tempo totale = len(df) * 0.3
    soglia_30 = len(df)*0.3
    
    # variabili
    n_fuori_range_hr = 0 # numero valori hr fuori range
    n_fuori_range_br = 0 # numero valori br fuori range
    n_fuori_range_peda = 0 # numero valori peda fuori range
    
    n_validi_hr = 0 # numero valori hr validi
    n_validi_br = 0 # numero valori br validi
    n_validi_peda = 0 # numero valori peda validi
    
    somma_validi_hr = 0 # somma valori hr validi
    somma_validi_br = 0 # somma valori br validi
    somma_validi_peda = 0 # somma valori peda validi
    
    media_hr = 0
    media_br = 0
    media_peda = 0
    
    sostituzioni = []
    
    # scorro tutte le righe
    for _, row in df.iterrows():
        # HR
        hr_val = row["Heart.Rate"]
        
        if hr_val < 40 or hr_val > 120: # valore hr fuori range
            n_fuori_range_hr += 1
            sostituzioni.append((row["Time"], "Heart.Rate"))
        else: # valore valido
            n_validi_hr += 1
            somma_validi_hr += hr_val
        
        # BR
        br_val = row["Breathing.Rate"]
        if br_val < 4 or br_val > 40: # valore fuori range
            n_fuori_range_br += 1
            sostituzioni.append((row["Time"], "Breathing.Rate"))
        else: # valore valido
            n_validi_br += 1
            somma_validi_br += br_val
        
        # PEDA
        peda_val = row["Palm.EDA"]
        if peda_val < 28 or peda_val > 628: # valore fuori range
            n_fuori_range_peda += 1
            sostituzioni.append((row["Time"], "Palm.EDA"))
        else: # valore valido
            n_validi_peda += 1
            somma_validi_peda += peda_val
        
    
    # calcolo media HR, BR, PEDA
    if n_validi_hr != 0:
        media_hr = somma_validi_hr / n_validi_hr
    if n_validi_br != 0:
        media_br = somma_validi_br / n_validi_br
    if n_validi_peda != 0:    
        media_peda = somma_validi_peda / n_validi_peda
        
        
    # valutazione soglia
    
    if n_fuori_range_hr >= soglia_30 or n_fuori_range_br >= soglia_30 or n_fuori_range_peda >= soglia_30:
        # conteggio >= 30% tempo totale -> eliminare la sessione
        return True
    else:
        # conteggio < 30% tempo totale -> sostituire valori fuori range con media corrispondente
        for tempo, tipo in sostituzioni:
            if tipo == "Heart.Rate":
                df.loc[df["Time"] == tempo, tipo] = media_hr
            if tipo == "Breathing.Rate":
                df.loc[df["Time"] == tempo, tipo] = media_br
            if tipo == "Palm.EDA":
                df.loc[df["Time"] == tempo, tipo] = media_peda
        return False
    
    
if __name__ == "__main__":
    main()