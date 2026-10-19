from pathlib import Path
from zipfile import ZipFile
import pandas as pd

pasta = Path("data/raw")
zip_path = pasta / "material_2026_09.csv.zip"


# Extrair o arquivo sem apagar o ZIP original
with ZipFile(zip_path, "r") as arquivo_zip:
    print("Arquivos dentro do ZIP:")
    print(arquivo_zip.namelist())
    arquivo_zip.extractall(pasta / "extraido")

# Localizar o CSV extraído
arquivos_csv = list((pasta / "extraido").rglob("*.csv"))

if not arquivos_csv:
    raise FileNotFoundError("Não foi encontrado nenhum CSV no ZIP.")

csv_path = arquivos_csv[0]
print("\nArquivo CSV:", csv_path)

# Ler inicialmente como texto para não alterar códigos e identificadores
df = pd.read_csv(
    csv_path,
    dtype=str,
    sep=None,
    engine="python",
    encoding="utf-8",
    on_bad_lines="error"
)

print("\nDimensões:", df.shape)
print("\nColunas:")
print(df.columns.tolist())

print("\nTipos e preenchimento:")
df.info()

print("\nPrimeiros registros:")
print(df.head(5).to_string(index=False))

print("\nValores nulos por coluna:")
print(df.isna().sum().sort_values(ascending=False))

print("\nLinhas completamente duplicadas:", df.duplicated().sum())