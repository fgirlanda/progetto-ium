# gestione NaN
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

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
    
    # separazione metadati/feature e estrazione gruppi (1 per soggetto) per `LeaveOneGroupOut` validation
    X_peda, y_peda, groups_peda = separate_columns(df_clean, "Palm.EDA")
    X_hr, y_hr, groups_hr = separate_columns(df_clean, "Heart.Rate")
    X_br, y_br, groups_br = separate_columns(df_clean, "Breathing.Rate")
    
    X_pereda, y_pereda, groups_pereda = separate_columns(df_clean, "Perinasal.Perspiration")
    
    # cf = classification
    cf_signals_datasets = { 
        "Palm.EDA":               (X_peda, y_peda, groups_peda),
        "Heart.Rate":             (X_hr, y_hr, groups_hr),
        "Breathing.Rate":         (X_br, y_br, groups_br),
        "Perinasal.Perspiration": (X_pereda, y_pereda, groups_pereda)
    }
    
    results = []
    for nome_segnale, (X, y, groups) in cf_signals_datasets.items():
        results.append((nome_segnale, five_fold_cf(X, y)))
    
    lista_righe = []
    for nome_segnale, res in results:
        lista_righe.append({
            "segnale": nome_segnale,
            **res
        })
        
    path_results = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data\\results'

    df_results = pd.DataFrame(lista_righe)
    generate_csv(df_results, path_results, "results")
        
        
def separate_columns(df: DataFrame, signal: str):
    df_signal = df[df["tipo_segnale"] == signal]
    X = df_signal.drop(columns=["id_soggetto", "tipo_segnale", "label"])
    y = df_signal["label"]
    
    groups = df_signal["id_soggetto"] # necessario per k-fold cross validation
    
    return X, y, groups


def five_fold_cf(X, y):
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits)
    
    knn_scores = []
    svm_scores = []
    
    for train_i, test_i in skf.split(X, y):
        X_train, X_test = X.iloc[train_i], X.iloc[test_i]
        y_train, y_test = y.iloc[train_i], y.iloc[test_i]

        # normalizzazione
        scaler = MinMaxScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        # KNN
        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(X_train, y_train)
        knn_scores.append(accuracy_score(y_test, knn.predict(X_test)))
        
        # SVM
        svm = SVC(kernel="rbf")
        svm.fit(X_train, y_train)
        svm_scores.append(accuracy_score(y_test, svm.predict(X_test)))
    
    return {
        "knn_mean": np.mean(knn_scores),
        "knn_std": np.std(knn_scores),
        "svm_mean": np.mean(svm_scores),
        "svm_std": np.std(svm_scores)
    }
        

def generate_csv(df: DataFrame, path_dir, nome_file): 
    # creare cartella se non esiste
    output = Path(path_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    # creare nuovo csv
    df.to_csv(output / (nome_file + ".csv"), index=False)
    

##############################################
# creazione dataset con feature concatenate


if __name__ == "__main__":
    main()