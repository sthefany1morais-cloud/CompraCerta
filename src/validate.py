from pathlib import Path
import pandas as pd

pasta_dados = Path("data") / "raw" / "extraido"
arquivo_csv = pasta_dados / "material_2026_09.csv"


def validar_dados():
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

    print("RELATORIO DE VALIDACAO")
    print("----------------------")
    print("Total de linhas:", len(dados))
    print("Total de colunas:", len(dados.columns))

    dados_limpos = dados.replace(r"^\s*$", pd.NA, regex=True)

    print("\nValores ausentes por coluna:")
    ausentes = dados_limpos.isna().sum()
    print(ausentes[ausentes > 0].sort_values(ascending=False))

    print("\nLinhas duplicadas completas:", dados.duplicated().sum())

    print(
        "\nIdentificadores de item ausentes:",
        dados_limpos["id_item_compra"].isna().sum()
    )

    print(
        "\nPrecos unitarios ausentes:",
        dados_limpos["preco_unitario"].isna().sum()
    )

    return dados