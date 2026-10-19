
from pathlib import Path
import pandas as pd

csv_path = next(Path("data/raw/extraido").rglob("*.csv"))

df = pd.read_csv(
    csv_path,
    dtype=str,
    encoding="utf-8-sig",
    sep=None,
    engine="python"
)

df.columns = [
    col.replace("\ufeff", "").strip().strip('"').strip("'")
    for col in df.columns
]

df = df.replace(r"^\s*$", pd.NA, regex=True)

# Investiga códigos de órgão com nomes diferentes
print("\n=== CONFLITOS: ÓRGÃO ===")

pares_orgao = (
    df[["codigo_orgao", "nome_orgao"]]
    .dropna()
    .drop_duplicates()
)

contagem_orgao = pares_orgao.groupby("codigo_orgao")["nome_orgao"].nunique()
codigos_orgao = contagem_orgao[contagem_orgao > 1].index

print(
    pares_orgao[pares_orgao["codigo_orgao"].isin(codigos_orgao)]
    .sort_values("codigo_orgao")
    .to_string(index=False)
)

# Investiga UASG com nomes diferentes
print("\n=== CONFLITOS: UASG ===")

pares_uasg = (
    df[["codigo_uasg", "nome_uasg", "codigo_orgao", "nome_orgao"]]
    .dropna(subset=["codigo_uasg", "nome_uasg"])
    .drop_duplicates()
)

contagem_uasg = pares_uasg.groupby("codigo_uasg")["nome_uasg"].nunique()
codigos_uasg = contagem_uasg[contagem_uasg > 1].index

print(
    pares_uasg[pares_uasg["codigo_uasg"].isin(codigos_uasg)]
    .sort_values("codigo_uasg")
    .to_string(index=False)
)

# Verifica os registros com preço ou quantidade igual a zero
print("\n=== PREÇOS IGUAIS A ZERO ===")

preco = pd.to_numeric(df["preco_unitario"], errors="coerce")
print(
    df.loc[preco.eq(0), [
        "id_item_compra", "id_compra", "numero_item_compra",
        "preco_unitario", "quantidade", "ni_fornecedor",
        "nome_fornecedor", "descricao_item"
    ]].to_string(index=False)
)

print("\n=== QUANTIDADES IGUAIS A ZERO ===")

quantidade = pd.to_numeric(df["quantidade"], errors="coerce")
print(
    df.loc[quantidade.eq(0), [
        "id_item_compra", "id_compra", "numero_item_compra",
        "preco_unitario", "quantidade", "descricao_item"
    ]].to_string(index=False)
)
