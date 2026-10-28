from pathlib import Path

arquivo_csv = Path("data") / "raw" / "extraido" / "material_2026_09.csv"


def carregar_dados():
    if not arquivo_csv.exists():
        print("Arquivo CSV nao encontrado:", arquivo_csv)
        return

    print("Arquivo CSV localizado:", arquivo_csv)
    print("Os dados estao prontos para uma carga controlada.")
    print("Nenhuma alteracao foi feita no banco de dados.")