import pandas as pd
import os

def main():
    origin = r'C:\\DEV\\MATLAB\\progetto-ium\\Risorse\\R-Friendly Study Data'
    dataframes = []
    
    with os.scandir(origin) as files:
        for file in files:
            df = extract_cols(file)
            if not check_missing_signals(df):
                dataframes.append(df)
    
    print(len(dataframes))

# scarta soggetti che non presentano uno dei segnali richiesti in nessun istante di tempo
def check_missing_signals(df):
    signals_cols = ["Palm.EDA", "Heart.Rate", "Breathing.Rate", "Perinasal.Perspiration"]
    if df[signals_cols].isnull().all().any(): 
        return True
    else:
        return False

def extract_cols(file):
    cols = ["Time", "Drive", "Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate", "Perinasal.Perspiration"]
    return pd.read_csv(file, usecols=cols)
    
    
if __name__ == "__main__":
    main()