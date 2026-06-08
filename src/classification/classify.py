# gestione NaN
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from sklearn.impute import SimpleImputer

def main():
    # leggere il csv in un dataframe
    path_raw = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data\\full_set\\full_set.csv'
    df_raw = pd.read_csv(path_raw)
    print(df_raw.isna().sum())
    print(len(df_raw))
    
    df_clean = df_raw.copy()
    # 23 righe nulle su 15120 le elimino
    df_clean = df_clean.dropna(subset=["four_moment", "five_moment", "kurtosis", "skew"]) 
    
    # rms e intervals_std NaN sostituiti con la media
    # data leakage, ma accettabile in quanto sono abbastanza stabili tra soggetti — non è un valore che cambia drasticamente tra training e test 
    
    imputer = SimpleImputer(strategy="mean")
    df_clean[["rmsd"]] = imputer.fit_transform(df_clean[["rmsd"]])
    df_clean[["intervals_std"]] = imputer.fit_transform(df_clean[["intervals_std"]])
    
    print(df_clean.isna().sum())
    print(len(df_clean))
    
    # dataframe pulito scritto su csv a parte
    path_clean = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data\\full_set'
    generate_csv(df_clean, path_clean, "full_set_clean")
    
    X_peda, y_peda, groups_peda = separate_columns(df_clean, "Palm.EDA")
    X_hr, y_hr, groups_hr = separate_columns(df_clean, "Heart.Rate")
    X_br, y_br, groups_br = separate_columns(df_clean, "Breathing.Rate")
    X_pereda, y_pereda, groups_pereda = separate_columns(df_clean, "Perinasal.Perspiration")
    
    

def separate_columns(df: DataFrame, signal: str):
    df_signal = df[df["tipo_segnale"] == signal]
    X = df_signal.drop(columns=["id_soggetto", "tipo_segnale", "label"])
    y = df_signal["label"]
    
    groups = df_signal["id_soggetto"] # necessario per k-fold cross validation
    
    return X, y, groups


def generate_csv(df: DataFrame, path_dir, nome_file): 
    # creare cartella se non esiste
    output = Path(path_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    # creare nuovo csv
    df.to_csv(output / (nome_file + ".csv"), index=False)
    

##############################################
# creazione dataset multimodal


if __name__ == "__main__":
    main()