import os
import time
import pandas as pd


def verificar_se_arquivo_excel_existe() -> bool:
    time.sleep(5)
    if os.path.exists(f"{os.getenv("Caminho_Pasta_Downloads")}\\challenge.xlsx"):
        return True
    else:
        return False


def excluir_arquivo_excel() -> None:
    try:
        os.remove(f"{os.getenv("Caminho_Pasta_Downloads")}\\challenge.xlsx")
    except:
        pass


def obter_data_frame_do_arquivo_excel() -> pd:
    data_frame = pd.read_excel(
        f"{os.getenv("Caminho_Pasta_Downloads")}\\challenge.xlsx"
    )
    return data_frame
