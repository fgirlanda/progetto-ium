# gestione NaN
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import LeaveOneGroupOut, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

from src.utility.utility import generate_csv

############################################################
# TODO
# multi-thread (?)
# separare knn e svm
############################################################

def main():
    path_results = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data\\results'
    
    # leggere il csv in un dataframe
    path_raw = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data\\full_set\\full_set.csv'
    df_raw = pd.read_csv(path_raw)
    # print(df_raw.isna().sum())
    # print(len(df_raw))
    
    df_clean = df_raw.copy()
    # 23 righe nulle su 15120 le elimino
    df_clean = df_clean.dropna(subset=["four_moment", "five_moment", "kurtosis", "skew"]) 
    
    # rms e intervals_std NaN sostituiti con la media -> !spostato dentro fold!
    # data leakage, ma accettabile in quanto sono abbastanza stabili tra soggetti — non è un valore che cambia drasticamente tra training e test 
    
    # imputer = SimpleImputer(strategy="mean")
    # df_clean[["rmsd"]] = imputer.fit_transform(df_clean[["rmsd"]])
    # df_clean[["intervals_std"]] = imputer.fit_transform(df_clean[["intervals_std"]])
    
    # print(df_clean.isna().sum())
    # print(len(df_clean))
    

    
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
    
    results_5fold = []
    results_loso = []
    for nome_segnale, (X, y, groups) in cf_signals_datasets.items():
        results_5fold.append((nome_segnale, five_fold_cf(X, y)))
        results_loso.append((nome_segnale, loso(X, y, groups)))
    
    lista_righe_5fold = []
    for nome_segnale, res in results_5fold:
        lista_righe_5fold.append({
            "segnale": nome_segnale,
            **res
        })
        
    lista_righe_loso = []
    for nome_segnale, res in results_loso:
        lista_righe_loso.append({
            "segnale": nome_segnale,
            **res
        })
        
    

    df_results_5fold = pd.DataFrame(lista_righe_5fold)
    generate_csv(df_results_5fold, path_results, "results_5fold")
    
    df_results_loso = pd.DataFrame(lista_righe_loso)
    generate_csv(df_results_loso, path_results, "results_loso")
    
    
    # dataframe con feature concatenate
    X_concat, y_concat, groups_concat = concatenate_signals(df_clean)
    
    results_loso_concat = loso(X_concat, y_concat, groups_concat)
    
    df_results_concat = pd.DataFrame([
        {
            "segnale": "ALL_SIGNALS",
            **results_loso_concat
        }
    ])
    
    generate_csv(df_results_concat, path_results, "results_loso_concat")
    
    # concatenazione di hr/br
    X_concat_hrbr, y_concat_hrbr, groups_concat_hrbr = concatenate_signals(df_clean, ["Heart.Rate", "Breathing.Rate"])
    
    results_loso_concat_hrbr = loso(X_concat_hrbr, y_concat_hrbr, groups_concat_hrbr)
    
    df_results_concat_hrbr = pd.DataFrame([
        {
            "segnale": "ALL_SIGNALS",
            **results_loso_concat_hrbr
        }
    ])
    
    generate_csv(df_results_concat_hrbr, path_results, "results_loso_concat_hrbr")
    

def concatenate_signals(df, signals=None):
    df_concat = df.copy()
    
    if signals:
        df_concat = df_concat[df_concat["tipo_segnale"].isin(signals)]
    
    # estraggo colonne feature
    feature_cols = [c for c in df_concat.columns if c not in ["id_soggetto", "t_corrente", "session_id", "tipo_segnale", "label"]]
    
    df_concat = df_concat.pivot(index=["id_soggetto", "t_corrente", "session_id", "label"], columns="tipo_segnale", values=feature_cols)
    
    df_concat = df_concat.dropna()
       
    df_concat.columns = [f"{signal}_{feature}" for feature, signal in df_concat.columns]
    
    df_concat = df_concat.reset_index()

    X = df_concat.drop(columns=["id_soggetto", "t_corrente", "label"]).dropna()

    y = df_concat["label"].dropna()

    groups = df_concat["id_soggetto"]
    
    return X, y, groups
    
        
def separate_columns(df: DataFrame, signal: str):
    df_signal = df[df["tipo_segnale"] == signal]
    X = df_signal.drop(columns=["id_soggetto", "t_corrente", "session_id", "tipo_segnale", "label"])
    y = df_signal["label"]
    
    groups = df_signal["id_soggetto"] # necessario per k-fold cross validation
    
    return X, y, groups


def five_fold_cf(X, y):
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits)
    
    knn_scores = []
    svm_scores = []
    
    for train_i, test_i in skf.split(X, y):
        X_train, X_test = X.iloc[train_i].copy(), X.iloc[test_i].copy()
        y_train, y_test = y.iloc[train_i].copy(), y.iloc[test_i].copy()
        
        rmsd_cols = [c for c in X_train.columns if "rmsd" in c]
        intervals_cols = [c for c in X_train.columns if "intervals_std" in c]
        nan_cols = rmsd_cols + intervals_cols

        imputer = SimpleImputer(strategy="mean")
        X_train[nan_cols] = imputer.fit_transform(X_train[nan_cols])
        X_test[nan_cols] = imputer.transform(X_test[nan_cols])


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
    
def loso(X, y, groups):
    logo = LeaveOneGroupOut()

    knn_scores = []
    svm_scores = []

    for train_i, test_i in logo.split(X, y, groups):

        X_train, X_test = X.iloc[train_i].copy(), X.iloc[test_i].copy()
        y_train, y_test = y.iloc[train_i].copy(), y.iloc[test_i].copy()
        
        rmsd_cols = [c for c in X_train.columns if "rmsd" in c]
        intervals_cols = [c for c in X_train.columns if "intervals_std" in c]
        nan_cols = rmsd_cols + intervals_cols

        imputer = SimpleImputer(strategy="mean")
        X_train[nan_cols] = imputer.fit_transform(X_train[nan_cols])
        X_test[nan_cols] = imputer.transform(X_test[nan_cols])

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
        
if __name__ == "__main__":
    main()