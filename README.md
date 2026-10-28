# CompraCerta

Projeto de análise e qualidade de dados de compras públicas, utilizando dados abertos do Compras.gov.br. O sistema permite investigar a qualidade dos dados e comparar preços de materiais a partir dos registros disponíveis.

## Objetivo

Explorar dados de pesquisa de preços de materiais de compras públicas, avaliar sua qualidade, investigar inconsistências e desenvolver uma aplicação que auxilie na consulta e comparação de preços.

## Fonte de dados

* **Portal:** Compras.gov.br — Dados Abertos
* **Arquivo:** `material_2026_09.csv.zip`
* **Período de referência:** setembro de 2026
* **Formato:** CSV compactado em ZIP
* **Registros analisados:** 100.957
* **Colunas da fonte:** 42

A descrição detalhada da origem está em [`docs/fonte_dos_dados.md`](docs/fonte_dos_dados.md).

## Funcionalidades

* Inspeção do arquivo original e de sua estrutura.
* Verificação de valores ausentes e linhas duplicadas.
* Investigação de inconsistências e possíveis duplicidades no catálogo de materiais.
* Documentação das regras e decisões de tratamento.
* Organização dos dados em tabelas relacionais no PostgreSQL.
* Pesquisa de materiais por parte da descrição.
* Comparação de preços por descrição exata, com cálculo do menor preço, maior preço, média e mediana.
* Exibição das até 20 ofertas com menores preços encontrados.

A diferença percentual entre a mediana e o menor preço é apresentada como referência estatística, não como garantia de economia real.

## Estrutura do projeto

* `app.py`: aplicação de console para pesquisa e comparação de preços.
* `data/raw/`: arquivos originais e arquivos extraídos.
* `data/processed/`: espaço para relatórios e arquivos derivados.
* `docs/`: documentação da fonte, regras de tratamento e relatório de qualidade.
* `notebooks/`: espaço para análises exploratórias.
* `scripts/`: scripts de carga, inspeção e investigação.
* `sql/`: consultas e documentação relacionada ao banco.
* `src/`: módulos de extração, transformação, carga e validação.
* `requirements.txt`: dependências Python do projeto.

## Tecnologias

* Python
* pandas
* SQLAlchemy
* psycopg
* PostgreSQL

## Configuração do ambiente

Na raiz do projeto, crie e ative o ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se o ambiente virtual já estiver ativo, não é necessário ativá-lo novamente.

## Banco de dados

O projeto utiliza PostgreSQL com o banco `compra_certa` e os schemas `staging` e `core`.

* **`staging`:** armazena os dados carregados da fonte original.
* **`core`:** contém as tabelas relacionais organizadas para consulta e análise.

A aplicação utiliza a variável de ambiente `DATABASE_URL` para estabelecer a conexão com o banco.

Antes de executar qualquer script de carga, verifique seu comportamento. O script `scripts/01_carregar_staging.py` utiliza `if_exists="replace"` no primeiro lote e pode substituir a tabela `staging.material_original`. Não execute esse script sobre uma base existente sem avaliar o impacto.

## Execução da aplicação

Com o ambiente virtual ativo e a variável `DATABASE_URL` configurada, execute:

```powershell
python app.py
```

O programa solicita o nome ou parte do nome de um material, apresenta as descrições encontradas e permite selecionar uma delas para consultar os preços.

A comparação considera ofertas com preço unitário positivo e sigla da unidade de fornecimento preenchida. Os resultados devem ser interpretados considerando as possíveis diferenças entre as condições de cada compra.

## Qualidade dos dados

As verificações e decisões realizadas estão documentadas em:

* [`docs/regras_tratamento.md`](docs/regras_tratamento.md)
* [`docs/relatorio_qualidade.md`](docs/relatorio_qualidade.md)

Os registros suspeitos não devem ser excluídos automaticamente. As decisões de tratamento devem considerar a origem, as evidências disponíveis e as regras documentadas.

## Estado do projeto

O projeto possui dados carregados no PostgreSQL, investigações de qualidade documentadas, consultas SQL e uma aplicação de console para comparação de preços.

A reprodução integral do processamento desde os dados originais até as tabelas relacionais ainda precisa ser verificada. A utilização dos schemas `staging` e `core` organiza os dados, mas não caracteriza, por si só, uma arquitetura de banco de dados distribuído.

## Cuidados

* Não versionar credenciais ou senhas.
* Preservar os arquivos originais sem alterações.
* Não executar scripts de carga sem verificar seus efeitos.
* Documentar as alterações e decisões de tratamento.
* Interpretar comparações de preços considerando as limitações dos dados disponíveis.
