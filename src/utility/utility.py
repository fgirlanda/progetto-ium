from pathlib import Path

from pandas import DataFrame


# crea un nuovo csv partendo dal df (df=dataframe, path=path cartella nuovo csv, name=nome del nuovo csv)

def generate_csv(df: DataFrame, path_dir, nome_file): 
    # creare cartella se non esiste
    output = Path(path_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    # creare nuovo csv
    df.to_csv(output / (nome_file + ".csv"), index=False)