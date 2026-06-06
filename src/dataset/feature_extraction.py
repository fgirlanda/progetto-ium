import os
import pandas as pd

def main():
    path = r'C:\\DEV\\MATLAB\\progetto-ium\\src\\data\\soggetti_in_range'
    with os.scandir(path) as subdirs:
        for dir_soggetto in subdirs:
            with os.scandir(dir_soggetto) as sessioni:
                for sessione in sessioni:
                    df = pd.read_csv(sessione)
                    print(df)
                    
                    break
            break
                    
    # parto da soggetti_in_range
    # per ogni soggetto (cartella)
        # per ogni file (sessione)
            # tipo (CD, PD, RD, ...)
            # per ogni segnale (colonna)
                # per ogni segmento
                    # estrarre segmento -> da tempo_corrente fino a min(tempo_corrente+60, tempo_totale)
                    # calcolo le feature
                    # passo al segmento successivo -> tempo_corrente += 30
    
    # struttura dati esterna -> lista
    
        # struttura dati interna -> tupla
    
            # soggetto -> int
            # classe stress/no-stress (ricavo dal tipo di sessione) -> boolean
            # segmenti (che contengono feature) -> tupla
                    
    pass

if __name__ == "__main__":
    main()