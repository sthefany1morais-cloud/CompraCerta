from pathlib import Path
from zipfile import ZipFile

pasta_projeto = Path(".")
pasta_dados = pasta_projeto / "data" / "raw"
arquivo_zip = pasta_dados / "material_2026_09.csv.zip"
pasta_destino = pasta_dados / "extraido"


def extrair_dados():
    if not arquivo_zip.exists():
        print("Arquivo zip nao encontrado:", arquivo_zip)
        return

    pasta_destino.mkdir(parents=True, exist_ok=True)

    with ZipFile(arquivo_zip, "r") as arquivo:
        arquivos_csv = [
            nome for nome in arquivo.namelist()
            if nome.lower().endswith(".csv")
        ]

        if not arquivos_csv:
            print("O arquivo zip nao contem nenhum CSV.")
            return

        for nome in arquivos_csv:
            destino = pasta_destino / Path(nome).name

            if destino.exists():
                print("Arquivo ja extraido:", destino)
                continue

            with arquivo.open(nome) as origem:
                destino.write_bytes(origem.read())

            print("Arquivo extraido:", destino)

    return pasta_destino