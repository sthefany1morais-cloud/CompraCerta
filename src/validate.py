from src.transform import transformar_dados


import pandas as pd


def validar_dados(dados):
    if dados is None:
        print("Validacao interrompida: dados indisponiveis.")
        return

    print("\nRELATORIO DE VALIDACAO")
    print("----------------------")
    print("Total de linhas:", len(dados))
    print("Total de colunas:", len(dados.columns))

    print(
        "\nIdentificadores de item ausentes:",
        int(dados["id_item_compra"].isna().sum())
    )

    print(
        "Identificadores de item distintos:",
        int(dados["id_item_compra"].nunique())
    )

    print(
        "\nLinhas duplicadas completas:",
        int(dados.duplicated().sum())
    )

    print("\nValores ausentes por coluna:")
    ausentes = dados.isna().sum()
    print(ausentes[ausentes > 0].sort_values(ascending=False))

    print(
        "\nRegistros com preco e quantidade zero:",
        int(dados["preco_e_quantidade_zero"].sum())
    )

    print(
        "Registros com preco ou quantidade zero:",
        int(dados["preco_ou_quantidade_zero"].sum())
    )

    print("\nValidacao concluida.")
    return dados