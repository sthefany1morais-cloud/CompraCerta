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


def buscar_unidades(descricao):
    consulta = text("""
        SELECT
            i.sigla_unidade_fornecimento,
            i.nome_unidade_fornecimento,
            i.capacidade_unidade_fornecimento,
            COUNT(*) AS total_ofertas
        FROM core.item_compra AS i
        JOIN core.catalogo_item AS c
            ON c.id_catalogo_item = i.id_catalogo_item
        WHERE c.descricao_item = :descricao
          AND i.preco_unitario > 0
          AND NULLIF(BTRIM(i.sigla_unidade_fornecimento), '') IS NOT NULL
        GROUP BY
            i.sigla_unidade_fornecimento,
            i.nome_unidade_fornecimento,
            i.capacidade_unidade_fornecimento
        ORDER BY
            i.sigla_unidade_fornecimento,
            i.nome_unidade_fornecimento,
            i.capacidade_unidade_fornecimento
    """)

    with engine.connect() as conexao:
        return conexao.execute(
            consulta, {"descricao": descricao}
        ).fetchall()


def pesquisar_precos(descricao):
    unidades = buscar_unidades(descricao)

    print(f"\nProduto selecionado: {descricao}")
    print("-" * 60)

    if not unidades:
        print("Nenhuma oferta válida com unidade informada.")
        return

    print("\nUnidades encontradas:")

    for indice, unidade in enumerate(unidades, start=1):
        nome = unidade.nome_unidade_fornecimento or "Nome não informado"

        print(
            f"{indice}. {unidade.sigla_unidade_fornecimento} - {nome} "
            f"| Capacidade: {unidade.capacidade_unidade_fornecimento} "
            f"| Ofertas: {unidade.total_ofertas}"
        )

    escolha = input(
        "\nEscolha a unidade e capacidade para comparar: "
    ).strip()

    if not escolha.isdigit():
        print("Digite um número válido.")
        return

    indice = int(escolha)

    if indice < 1 or indice > len(unidades):
        print("Opção fora da lista.")
        return

    unidade_escolhida = unidades[indice - 1]

    parametros = {
        "descricao": descricao,
        "sigla": unidade_escolhida.sigla_unidade_fornecimento,
        "nome_unidade": unidade_escolhida.nome_unidade_fornecimento,
        "capacidade": unidade_escolhida.capacidade_unidade_fornecimento,
    }

    consulta_resumo = text("""
        WITH estatisticas AS (
            SELECT
                COUNT(*) AS n,
                PERCENTILE_CONT(0.25)
                    WITHIN GROUP (ORDER BY i.preco_unitario) AS q1,
                PERCENTILE_CONT(0.75)
                    WITHIN GROUP (ORDER BY i.preco_unitario) AS q3
            FROM core.item_compra AS i
            JOIN core.catalogo_item AS c
                ON c.id_catalogo_item = i.id_catalogo_item
            WHERE c.descricao_item = :descricao
              AND i.preco_unitario > 0
              AND i.sigla_unidade_fornecimento = :sigla
              AND i.nome_unidade_fornecimento
                  IS NOT DISTINCT FROM :nome_unidade
              AND i.capacidade_unidade_fornecimento
                  IS NOT DISTINCT FROM :capacidade
        ),
        limites AS (
            SELECT
                n,
                GREATEST(0::numeric, q1 - 1.5 * (q3 - q1))
                    AS limite_inferior,
                q3 + 1.5 * (q3 - q1) AS limite_superior
            FROM estatisticas
        )
        SELECT
            COUNT(*) AS total_ofertas,
            MIN(i.preco_unitario) AS menor_preco,
            MAX(i.preco_unitario) AS maior_preco,
            ROUND(AVG(i.preco_unitario), 2) AS preco_medio,
            PERCENTILE_CONT(0.5)
                WITHIN GROUP (ORDER BY i.preco_unitario)
                AS mediana_preco,
            CASE
                WHEN l.n < 5 THEN NULL
                ELSE COUNT(*) FILTER (
                    WHERE i.preco_unitario < l.limite_inferior
                       OR i.preco_unitario > l.limite_superior
                )
            END AS total_atipicos,
            CASE
                WHEN l.n < 5 THEN NULL
                ELSE COUNT(*) FILTER (
                    WHERE i.preco_unitario >= l.limite_inferior
                      AND i.preco_unitario <= l.limite_superior
                )
            END AS total_dentro_padrao,
            l.limite_inferior,
            l.limite_superior
        FROM core.item_compra AS i
        JOIN core.catalogo_item AS c
            ON c.id_catalogo_item = i.id_catalogo_item
        CROSS JOIN limites AS l
        WHERE c.descricao_item = :descricao
          AND i.preco_unitario > 0
          AND i.sigla_unidade_fornecimento = :sigla
          AND i.nome_unidade_fornecimento
              IS NOT DISTINCT FROM :nome_unidade
          AND i.capacidade_unidade_fornecimento
              IS NOT DISTINCT FROM :capacidade
        GROUP BY
            l.n,
            l.limite_inferior,
            l.limite_superior
    """)

    consulta_ofertas = text("""
        WITH estatisticas AS (
            SELECT
                COUNT(*) AS n,
                PERCENTILE_CONT(0.25)
                    WITHIN GROUP (ORDER BY i.preco_unitario) AS q1,
                PERCENTILE_CONT(0.50)
                    WITHIN GROUP (ORDER BY i.preco_unitario) AS mediana,
                PERCENTILE_CONT(0.75)
                    WITHIN GROUP (ORDER BY i.preco_unitario) AS q3
            FROM core.item_compra AS i
            JOIN core.catalogo_item AS c
                ON c.id_catalogo_item = i.id_catalogo_item
            WHERE c.descricao_item = :descricao
              AND i.preco_unitario > 0
              AND i.sigla_unidade_fornecimento = :sigla
              AND i.nome_unidade_fornecimento
                  IS NOT DISTINCT FROM :nome_unidade
              AND i.capacidade_unidade_fornecimento
                  IS NOT DISTINCT FROM :capacidade
        ),
        limites AS (
            SELECT *,
                GREATEST(
                    0::numeric,
                    q1 - 1.5 * (q3 - q1)
                ) AS limite_inferior,
                q3 + 1.5 * (q3 - q1) AS limite_superior
            FROM estatisticas
        )
        SELECT
            i.nome_fornecedor,
            i.preco_unitario,
            i.sigla_unidade_fornecimento,
            i.nome_unidade_fornecimento,
            i.capacidade_unidade_fornecimento,
            i.quantidade,
            i.id_compra,
            l.n AS quantidade_precos,
            l.mediana,
            l.limite_inferior,
            l.limite_superior,
            CASE
                WHEN l.n < 5 THEN 'AMOSTRA INSUFICIENTE'
                WHEN i.preco_unitario < l.limite_inferior
                    THEN 'POSSIVEL PRECO ATIPICO - ABAIXO'
                WHEN i.preco_unitario > l.limite_superior
                    THEN 'POSSIVEL PRECO ATIPICO - ACIMA'
                ELSE 'DENTRO DO PADRAO'
            END AS classificacao
        FROM core.item_compra AS i
        JOIN core.catalogo_item AS c
            ON c.id_catalogo_item = i.id_catalogo_item
        CROSS JOIN limites AS l
        WHERE c.descricao_item = :descricao
          AND i.preco_unitario > 0
          AND i.sigla_unidade_fornecimento = :sigla
          AND i.nome_unidade_fornecimento
              IS NOT DISTINCT FROM :nome_unidade
          AND i.capacidade_unidade_fornecimento
              IS NOT DISTINCT FROM :capacidade
        ORDER BY i.preco_unitario ASC
        LIMIT 20
    """)

    with engine.connect() as conexao:
        resumo = conexao.execute(
            consulta_resumo, parametros
        ).fetchone()

        ofertas = conexao.execute(
            consulta_ofertas, parametros
        ).fetchall()

    print("\nComparação de preços")
    print("-" * 60)

    if not resumo or resumo.total_ofertas == 0:
        print("Nenhuma oferta válida encontrada.")
        return

    menor = float(resumo.menor_preco)
    maior = float(resumo.maior_preco)
    media = float(resumo.preco_medio)
    mediana = float(resumo.mediana_preco)

    diferenca_percentual = (
        (mediana - menor) / mediana * 100
        if mediana > 0 else 0
    )

    print(f"Total de ofertas: {resumo.total_ofertas}")
    print(f"Menor preço: R$ {menor:.2f}")
    print(f"Maior preço: R$ {maior:.2f}")
    print(f"Preço médio: R$ {media:.2f}")
    print(f"Mediana dos preços: R$ {mediana:.2f}")

    print("\nAnálise estatística dos preços")
    print("-" * 60)

    if resumo.total_atipicos is not None:
        print(f"Preços possivelmente atípicos: {resumo.total_atipicos}")
        print(f"Preços dentro do padrão: {resumo.total_dentro_padrao}")
        print(f"Limite inferior do IQR: R$ {float(resumo.limite_inferior):.2f}")
        print(f"Limite superior do IQR: R$ {float(resumo.limite_superior):.2f}")
        print(
            f"Total classificado: "
            f"{resumo.total_atipicos + resumo.total_dentro_padrao}"
        )
    else:
        print(
            "Amostra insuficiente para classificar os preços "
            "pelo método IQR (menos de 5 ofertas)."
        )

    print(
        f"Diferença entre a mediana e o menor preço: "
        f"{diferenca_percentual:.2f}%"
    )

    print("\nOfertas e sinalização estatística")
    print("-" * 60)

    for item in ofertas:
        print(f"Fornecedor: {item.nome_fornecedor}")
        print(f"Preço unitário: R$ {float(item.preco_unitario):.2f}")
        print(f"Unidade: {item.sigla_unidade_fornecimento}")
        print(
            f"Nome da unidade: "
            f"{item.nome_unidade_fornecimento or 'Não informado'}"
        )
        print(f"Quantidade: {float(item.quantidade or 0):,.2f}")
        print(f"Compra: {item.id_compra}")
        print(f"Classificação: {item.classificacao}")

        if item.quantidade_precos >= 5:
            print(
                f"Limite inferior IQR: "
                f"R$ {float(item.limite_inferior):.2f}"
            )
            print(
                f"Limite superior IQR: "
                f"R$ {float(item.limite_superior):.2f}"
            )
        else:
            print("Poucos preços para uma avaliação estatística confiável.")

        print("-" * 60)

    print(
        "\nO método IQR sinaliza possíveis valores atípicos. "
        "Um alerta não comprova erro ou irregularidade."
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
