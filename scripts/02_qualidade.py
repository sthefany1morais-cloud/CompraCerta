import pandas as pd
from pathlib import Path

csv_path = next(
    Path("data/raw/extraido").rglob("*.csv")
)

df = pd.read_csv(
    csv_path,
    dtype=str,
    sep=None,
    engine="python",
    encoding="utf-8"
)

relatorio = pd.DataFrame({
    "tipo": df.dtypes.astype(str),
    "nulos": df.isna().sum(),
    "percentual_nulos": (
        df.isna().mean() * 100
    ).round(2),
    "valores_distintos": df.nunique(dropna=True)
})

Path("data/processed").mkdir(
    parents=True, exist_ok=True
)

relatorio.to_csv(
    "data/processed/relatorio_qualidade.csv",
    encoding="utf-8"
)

print(relatorio.to_string())
print("\nDuplicatas completas:", df.duplicated().sum())