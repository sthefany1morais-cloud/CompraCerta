from pathlib import Path
import pandas as pd

pasta_dados = Path("data") / "raw" / "extraido"
arquivo_csv = pasta_dados / "material_2026_09.csv"


def transformar_dados():
    if not arquivo_csv.exists():
        print("Arquivo CSV nao encontrado:", arquivo_csv)
        return

    dados = pd.read_csv(
        arquivo_csv,
        sep=";",
        dtype=str,
        encoding="utf-8",
        low_memory=False
    )

    dados.columns = [
        coluna.strip().lower()
        for coluna in dados.columns
    ]

    print("Arquivo carregado para analise.")
    print("Quantidade de linhas:", len(dados))
    print("Quantidade de colunas:", len(dados.columns))
    print("Colunas encontradas:")
    print(list(dados.columns))

    return dados