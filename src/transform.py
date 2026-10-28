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

    # Converte valores vazios ou compostos por espaços em ausentes.
    dados = dados.replace(r"^\s*$", pd.NA, regex=True)

    # Converte campos numéricos para permitir validações.
    for coluna in ["preco_unitario", "quantidade"]:
        if coluna in dados.columns:
            dados[coluna] = pd.to_numeric(
                dados[coluna],
                errors="coerce"
            )

    # Sinaliza registros com preço ou quantidade iguais a zero.
    dados["preco_ou_quantidade_zero"] = (
            dados["preco_unitario"].eq(0)
            | dados["quantidade"].eq(0)
    )

    # Sinaliza os quatro casos investigados, sem excluir registros.
    dados["preco_e_quantidade_zero"] = (
            dados["preco_unitario"].eq(0)
            & dados["quantidade"].eq(0)
    )

    print("Transformacao concluida.")
    print("Quantidade de linhas:", len(dados))
    print("Quantidade de colunas:", len(dados.columns))
    print(
        "Registros com preco ou quantidade zero:",
        int(dados["preco_ou_quantidade_zero"].sum())
    )
    print(
        "Registros com preco e quantidade zero:",
        int(dados["preco_e_quantidade_zero"].sum())
    )

    return dados