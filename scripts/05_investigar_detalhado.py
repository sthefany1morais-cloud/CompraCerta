
from pathlib import Path
import pandas as pd

# Localiza o CSV extraído
csv_path = next(Path("data/raw/extraido").rglob("*.csv"))

df = pd.read_csv(
    csv_path,
    dtype=str,
    encoding="utf-8-sig",
    sep=None,
    engine="python"
)

# Padroniza os nomes das colunas
df.columns = [
    col.replace("\ufeff", "").strip().strip('"').strip("'")
    for col in df.columns
]

# Converte strings vazias e espaços em valores ausentes
df = df.replace(r"^\s*$", pd.NA, regex=True)

print("\n=== 1. ESTADOS FORA DO PADRÃO ESPERADO ===")
print(df.loc[df["estado"] == "EX", [
    "estado", "codigo_municipio", "municipio",
    "codigo_uasg", "nome_uasg", "nome_orgao"
]].to_string(index=False))

print("\n=== 2. ID_COMPRA_ITEM REPETIDOS ===")
repetidos = df[
    df["id_compra_item"].duplicated(keep=False)
].sort_values("id_compra_item")

print("Total de linhas com ID repetido:", len(repetidos))
print("Quantidade de IDs repetidos:",
      repetidos["id_compra_item"].nunique())

print(repetidos[[
    "id_compra_item", "id_item_compra", "id_compra",
    "numero_item_compra", "ni_fornecedor",
    "nome_fornecedor", "preco_unitario"
]].head(30).to_string(index=False))

print("\n=== 3. PREÇOS E QUANTIDADES ===")

for coluna in ["preco_unitario", "quantidade"]:
    valores = pd.to_numeric(df[coluna], errors="coerce")
    invalidos = valores.isna()
    negativos = valores < 0
    zeros = valores == 0

    print(f"\nCampo: {coluna}")
    print("Valores ausentes ou não numéricos:", int(invalidos.sum()))
    print("Valores negativos:", int(negativos.sum()))
    print("Valores iguais a zero:", int(zeros.sum()))

    print("Exemplos não numéricos:")
    print(df.loc[invalidos, coluna].head(10).to_list())

print("\n=== 4. CAMPOS COM MAIS VALORES AUSENTES ===")
ausentes = df.isna().sum().sort_values(ascending=False)
print(ausentes[ausentes > 0].to_string())

print("\n=== 5. RELAÇÕES ENTRE CÓDIGO E NOME ===")

for codigo, nome in [
    ("codigo_municipio", "municipio"),
    ("codigo_orgao", "nome_orgao"),
    ("codigo_uasg", "nome_uasg"),
    ("codigo_classe", "nome_classe"),
    ("codigo_grupo", "nome_grupo"),
    ("codigo_pdm", "nome_pdm"),
]:
    pares = df[[codigo, nome]].dropna().drop_duplicates()
    contagem = pares.groupby(codigo)[nome].nunique()
    conflitos = contagem[contagem > 1]

    print(f"\n{codigo} -> {nome}")
    print("Códigos associados a mais de um nome:",
          len(conflitos))
    if not conflitos.empty:
        print(conflitos.head(10).to_string())

# Salva uma amostra dos registros repetidos para inspeção
Path("data/processed").mkdir(parents=True, exist_ok=True)
repetidos.to_csv(
    "data/processed/id_compra_item_repetidos.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nAnálise concluída.")
print("Amostra completa dos IDs repetidos salva em:")
print("data/processed/id_compra_item_repetidos.csv")
