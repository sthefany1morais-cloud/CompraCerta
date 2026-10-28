import os
from sqlalchemy import create_engine, text

engine = create_engine(os.environ["DATABASE_URL"])


def buscar_descricoes(termo):
    consulta = text("""
        SELECT DISTINCT descricao_item
        FROM core.catalogo_item
        WHERE descricao_item ILIKE :termo
          AND descricao_item IS NOT NULL
          AND BTRIM(descricao_item) <> ''
        ORDER BY descricao_item
        LIMIT 30
    """)

    with engine.connect() as conexao:
        return conexao.execute(
            consulta, {"termo": f"%{termo}%"}
        ).scalars().all()


def pesquisar_precos(descricao):
    consulta_resumo = text("""
        SELECT
            COUNT(*) AS total_ofertas,
            MIN(i.preco_unitario) AS menor_preco,
            MAX(i.preco_unitario) AS maior_preco,
            ROUND(AVG(i.preco_unitario), 2) AS preco_medio,
            PERCENTILE_CONT(0.5)
                WITHIN GROUP (ORDER BY i.preco_unitario)
                AS mediana_preco
        FROM core.item_compra AS i
        JOIN core.catalogo_item AS c
            ON c.id_catalogo_item = i.id_catalogo_item
        WHERE c.descricao_item = :descricao
          AND i.preco_unitario > 0
          AND i.sigla_unidade_fornecimento IS NOT NULL
    """)

    consulta_ofertas = text("""
        SELECT
            i.nome_fornecedor,
            i.preco_unitario,
            i.sigla_unidade_fornecimento,
            i.nome_unidade_fornecimento,
            i.quantidade,
            i.id_compra
        FROM core.item_compra AS i
        JOIN core.catalogo_item AS c
            ON c.id_catalogo_item = i.id_catalogo_item
        WHERE c.descricao_item = :descricao
          AND i.preco_unitario > 0
          AND i.sigla_unidade_fornecimento IS NOT NULL
        ORDER BY i.preco_unitario ASC
        LIMIT 20
    """)

    parametros = {"descricao": descricao}

    with engine.connect() as conexao:
        resumo = conexao.execute(
            consulta_resumo, parametros
        ).fetchone()

        ofertas = conexao.execute(
            consulta_ofertas, parametros
        ).fetchall()

    print(f"\nProduto selecionado: {descricao}")
    print("-" * 55)

    if resumo.total_ofertas == 0:
        print("Nenhuma oferta válida encontrada.")
        return

    menor = float(resumo.menor_preco)
    maior = float(resumo.maior_preco)
    media = float(resumo.preco_medio)
    mediana = float(resumo.mediana_preco)

    economia_percentual = (
        (mediana - menor) / mediana * 100
        if mediana > 0 else 0
    )

    print(f"Total de ofertas: {resumo.total_ofertas}")
    print(f"Menor preço: R$ {menor:.2f}")
    print(f"Maior preço: R$ {maior:.2f}")
    print(f"Preço médio: R$ {media:.2f}")
    print(f"Mediana dos preços: R$ {mediana:.2f}")
    print(
        f"Diferença entre a mediana e o menor preço: "
        f"{economia_percentual:.2f}%"
    )

    print("\nAté 20 ofertas com menor preço")
    print("-" * 55)

    for item in ofertas:
        print(f"Fornecedor: {item.nome_fornecedor}")
        print(f"Preço: R$ {float(item.preco_unitario):.2f}")
        print(
            f"Unidade: {item.sigla_unidade_fornecimento} - "
            f"{item.nome_unidade_fornecimento or 'Não informada'}"
        )
        print(f"Quantidade: {float(item.quantidade or 0):,.2f}")
        print(f"Compra: {item.id_compra}")
        print("-" * 55)

    print(
        "\nObservação: a diferença percentual é uma referência "
        "estatística, não uma garantia de economia real."
    )


def executar():
    termo = input("Digite o nome ou parte do produto: ").strip()

    if not termo:
        print("Digite um termo para pesquisar.")
        return

    descricoes = buscar_descricoes(termo)

    if not descricoes:
        print("Nenhum produto encontrado.")
        return

    print("\nDescrições encontradas:")
    for indice, descricao in enumerate(descricoes, start=1):
        print(f"{indice}. {descricao}")

    escolha = input(
        "\nDigite o número da descrição que deseja comparar: "
    ).strip()

    if not escolha.isdigit():
        print("Digite um número válido.")
        return

    indice = int(escolha)

    if indice < 1 or indice > len(descricoes):
        print("Opção fora da lista.")
        return

    pesquisar_precos(descricoes[indice - 1])


if __name__ == "__main__":
    try:
        executar()
    finally:
        engine.dispose()