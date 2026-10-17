from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine

csv_path = next(
    Path("data/raw/extraido").rglob("*.csv")
)

# Configure a variável DATABASE_URL antes de executar.
# Exemplo de formato:
# postgresql+psycopg://usuario:senha@localhost:5432/compra_certa
database_url = os.environ["DATABASE_URL"]

engine = create_engine(database_url)

# Ajuste o tamanho do lote conforme a memória disponível.
lote = 10_000
primeiro_lote = True

for parte in pd.read_csv(
    csv_path,
    dtype=str,
    sep=None,
    engine="python",
    encoding="utf-8",
    chunksize=lote
):
    parte.to_sql(
        "material_original",
        engine,
        schema="staging",
        if_exists="replace" if primeiro_lote else "append",
        index=False,
        chunksize=1000,
        method="multi"
    )

    primeiro_lote = False
    print(f"Lote importado: {len(parte)} linhas")

print("Importação concluída.")