from pathlib import Path

from pandas import DataFrame

SESSIONS = {
        # 1: "B",
        2: "PD",
        3: "RD",
        4: "LD",
        5: "CD",
        6: "ED",
        7: "MD"
        # 8: "FDN/FDL/..."
    }

def get_project_root():
    project_root = Path(__file__).resolve()
    while project_root.name != "progetto-ium":
        project_root = project_root.parent
    
    return project_root

# crea un nuovo csv partendo dal df (df=dataframe, path=path cartella nuovo csv, name=nome del nuovo csv)
def generate_csv(df: DataFrame, path_dir, nome_file): 
    # creare cartella se non esiste
    output = Path(path_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    # creare nuovo csv
    df.to_csv(output / (nome_file + ".csv"), index=False)