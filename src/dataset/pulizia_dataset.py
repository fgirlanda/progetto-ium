from pathlib import Path

import pandas as pd
import os

def main():
    origin = r'C:\\DEV\\MATLAB\\progetto-ium\\Risorse\\R-Friendly Study Data'
    output_dir = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data'
    dataframes = []
    
    with os.scandir(origin) as files:
        for file in files:
            df = extract_cols(file)
            generate_csv(df, output_dir + "\\without_car_data", Path(file.name).stem+"no_car") # csv senza colonne irrilevanti
            if not check_missing_signals(df):
                dataframes.append((Path(file.name).stem, df))
    
    for name, dataframe in dataframes:
        generate_csv(dataframe, output_dir + "\\deleted_missing", name+"data_exists") # csv senza soggetti con segnali mancanti
    
    for name, dataframe in dataframes:
        extract_measures(dataframe)

# NON legge colonne non relative a segnali di interesse
def extract_cols(file):
    cols = ["Time", "Drive", "Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate", "Perinasal.Perspiration"]
    return pd.read_csv(file, usecols=cols)

# scarta soggetti che non presentano uno dei segnali richiesti in nessun istante di tempo
def check_missing_signals(df):
    signals_cols = ["Palm.EDA", "Heart.Rate", "Breathing.Rate", "Perinasal.Perspiration"]
    if df[signals_cols].isnull().all().any(): 
        return True
    else:
        return False
    
# estrae singole misurazioni per ogni soggetto
def extract_measures(df):
    pass


# crea un nuovo csv partendo dal df (df=dataframe, path=path cartella nuovo csv, name=nome del nuovo csv)
def generate_csv(df, path, name): 
    # creare cartella se non esiste
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    
    # creare nuovo csv
    df.to_csv(output / (name + ".csv"), index=False)

    
    
if __name__ == "__main__":
    main()