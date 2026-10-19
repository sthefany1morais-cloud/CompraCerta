
from pathlib import Path
import pandas as pd

csv_path = next(Path("data/raw/extraido").rglob("*.csv"))

df = pd.read_csv(
    csv_path,
    dtype=str,
    sep=None,
    engine="python",
    encoding="utf-8-sig"
)

# Corrigir cabeçalhos com BOM e aspas extras
df.columns = [
    col.replace("\ufeff", "").strip().strip('"').strip("'")
    for col in df.columns
]

print("Dimensões:", df.shape)
print("Colunas:", df.columns.tolist())

# Investigar valores inesperados em campos categóricos
for coluna in [
    "estado", "poder", "esfera", "forma",
    "modalidade", "criterio_julgamento",
    "sigla_unidade_fornecimento"
]:
    if coluna in df.columns:
        print(f"\n--- {coluna} ---")
        print(df[coluna].value_counts(dropna=False).head(40))

# Verificar identificadores repetidos
for coluna in [
    "id_item_compra", "id_compra_item",
    "id_compra", "codigo_uasg", "ni_fornecedor"
]:
    if coluna in df.columns:
        print(f"\n--- {coluna} ---")
        print("Linhas:", len(df))
        print("Valores distintos:", df[coluna].nunique(dropna=True))
        print("Linhas com valor repetido:",
              df[coluna].duplicated(keep=False).sum())

# Verificar relação entre código e nome do município
if {"codigo_municipio", "municipio"}.issubset(df.columns):
    municipios = df[
        ["codigo_municipio", "municipio"]
    ].dropna().drop_duplicates()

    print("\nCódigos associados a vários nomes:")
    print(
        municipios.groupby("codigo_municipio")["municipio"]
        .nunique().sort_values(ascending=False).head(20)
    )

# Salvar uma amostra corrigida para a próxima etapa
Path("data/processed").mkdir(parents=True, exist_ok=True)

df.head(1000).to_csv(
    "data/processed/amostra_inspecao.csv",
    index=False,
    encoding="utf-8"
)