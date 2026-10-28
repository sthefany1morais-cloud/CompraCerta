from src.extract import extrair_dados
from src.transform import transformar_dados
from src.validate import validar_dados


def processar_dados():
    print("\nETAPA 1 — EXTRAÇÃO")
    pasta = extrair_dados()

    if pasta is None:
        print("Processamento interrompido na extração.")
        return

    print("\nETAPA 2 — TRANSFORMAÇÃO")
    dados = transformar_dados()

    if dados is None:
        print("Processamento interrompido na transformação.")
        return

    print("\nETAPA 3 — VALIDAÇÃO")
    dados_validados = validar_dados()

    if dados_validados is None:
        print("Processamento interrompido na validação.")
        return

    print("\nProcessamento concluído.")
    print(f"Linhas transformadas: {len(dados)}")
    print(f"Linhas validadas: {len(dados_validados)}")
    print("Nenhuma alteração foi feita no banco de dados.")


if __name__ == "__main__":
    processar_dados()