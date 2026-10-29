# CompraCerta

Projeto de análise da qualidade dos dados e comparação de preços em compras públicas, utilizando dados abertos do Compras.gov.br. O sistema permite investigar inconsistências nos registros e comparar preços de materiais, auxiliando na análise das ofertas disponíveis.

## 1. Objetivo

Explorar dados de pesquisas de preços de materiais de compras públicas, avaliar sua qualidade, investigar possíveis inconsistências e desenvolver uma aplicação que permita consultar e comparar preços.

## 2. Fonte de dados

* **Portal:** Compras.gov.br — Dados Abertos
* **Arquivo:** `material_2026_09.csv.zip`
* **Período de referência:** setembro de 2026
* **Formato:** CSV compactado em ZIP
* **Registros analisados:** 100.957
* **Colunas da fonte:** 42

A descrição detalhada da origem dos dados está em [`docs/fonte_dos_dados.md`](docs/fonte_dos_dados.md).

## 3. Funcionalidades

O projeto contempla:

* Inspeção do arquivo original e de sua estrutura.
* Verificação de valores ausentes e linhas duplicadas.
* Investigação de inconsistências e possíveis duplicidades no catálogo de materiais.
* Documentação das regras e decisões de tratamento.
* Organização dos dados em tabelas relacionais no PostgreSQL.
* Pesquisa de materiais por parte da descrição.
* Seleção de uma descrição de material para consulta.
* Comparação de preços por material, unidade de fornecimento e capacidade.
* Cálculo do menor preço, maior preço, média e mediana.
* Cálculo de limites estatísticos pelo método do intervalo interquartil (IQR).
* Identificação de possíveis preços atípicos abaixo ou acima dos limites calculados.
* Apresentação das até 20 ofertas com menores preços encontrados.
* Exibição da quantidade de ofertas classificadas como atípicas ou dentro do padrão, quando há amostra suficiente.

A diferença percentual entre a mediana e o menor preço é apresentada como referência estatística, não como garantia de economia real.

As classificações pelo IQR são indicativos estatísticos e não comprovam, isoladamente, erros ou irregularidades.

## 4. Estrutura do projeto

A estrutura planejada e documentada do repositório é:

* `app.py`: aplicação de console para pesquisa e comparação de preços.
* `data/raw/`: arquivos originais e arquivos extraídos.
* `data/processed/`: espaço para relatórios e arquivos derivados.
* `docs/`: documentação da fonte, regras de tratamento e relatório de qualidade.
* `notebooks/`: espaço para análises exploratórias.
* `scripts/`: scripts de carga, inspeção e investigação.
* `sql/`: consultas SQL e documentação relacionada ao banco.
* `src/`: módulos de extração, transformação, carga e validação.
* `requirements.txt`: dependências Python do projeto.

A presença e o conteúdo de cada arquivo ou diretório devem ser conferidos no repositório antes de considerar a estrutura integralmente reproduzível.

## 5. Tecnologias utilizadas

* Python
* pandas
* SQLAlchemy
* psycopg
* PostgreSQL

## 6. Banco de dados

O projeto utiliza o PostgreSQL com o banco `compra_certa` e os schemas `staging` e `core`.

### 6.1. Schema `staging`

O schema `staging` é utilizado para armazenar os dados recebidos da fonte original antes de sua organização e transformação.

A tabela identificada é:

* `staging.material_original`: armazena os registros importados da fonte de dados.

### 6.2. Schema `core`

O schema `core` contém as tabelas relacionais utilizadas nas consultas e análises:

* `core.catalogo_item`: catálogo de materiais.
* `core.compra`: informações das compras.
* `core.fornecedor`: informações dos fornecedores.
* `core.item_compra`: itens e preços registrados nas compras.
* `core.localidade`: informações geográficas.
* `core.orgao`: informações dos órgãos responsáveis pelas compras.
* `core.sinonimo_item`: termos alternativos para auxiliar na pesquisa de materiais.
* `core.unidade_compradora`: informações das unidades compradoras.

### 6.3. Views de análise

O banco também possui as seguintes views:

* `core.vw_comparacao_precos`: reúne informações para a comparação de preços.
* `core.vw_inconsistencias_item`: auxilia na investigação de possíveis inconsistências.
* `core.vw_precos_suspeitos`: auxilia na identificação de preços que merecem análise adicional.

As chaves primárias, as chaves estrangeiras e os relacionamentos entre as tabelas ainda devem ser conferidos diretamente no banco para completar a documentação do modelo relacional.

## 7. Tratamento e qualidade dos dados

O processamento separa os dados originais dos dados organizados para consulta. As regras e decisões de tratamento estão documentadas em:

* [`docs/regras_tratamento.md`](docs/regras_tratamento.md)
* [`docs/relatorio_qualidade.md`](docs/relatorio_qualidade.md)

Entre os aspectos investigados estão valores ausentes, possíveis duplicidades, inconsistências nos registros e valores de preços que merecem verificação.

Os registros suspeitos não devem ser excluídos automaticamente. As decisões de tratamento precisam considerar a origem, as evidências disponíveis e as regras documentadas.

### 7.1. Critérios da comparação de preços

A comparação realizada pela aplicação considera ofertas com preço unitário positivo e sigla da unidade de fornecimento preenchida.

Os preços são agrupados de acordo com o material selecionado, a unidade e a capacidade utilizada na consulta. A interpretação dos resultados deve considerar as possíveis diferenças entre as condições de cada compra.

### 7.2. Método IQR

O método do intervalo interquartil é utilizado para estabelecer limites estatísticos com base nos quartis dos preços observados.

A aplicação classifica os preços abaixo do limite inferior ou acima do limite superior como possíveis valores atípicos. Os preços dentro dos limites são classificados como dentro do padrão estatístico do grupo.

Quando a quantidade de ofertas é inferior a cinco, a amostra é considerada insuficiente para essa classificação na aplicação.

Uma classificação estatística não comprova que um preço está incorreto. Os resultados devem ser interpretados como indicadores para investigação adicional.

### 7.3. Registros com preço zero

Foram identificados quatro registros com preço zero e quantidade igual a zero no conjunto analisado.

Esses registros são preservados para investigação e documentação. Não são classificados automaticamente como erros, pois a interpretação depende do contexto e da origem dos dados.

## 8. Configuração do ambiente

Na raiz do projeto, crie e ative um ambiente virtual e instale as dependências.

No PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se o ambiente virtual já estiver ativo, não é necessário ativá-lo novamente.

## 9. Configuração da conexão com o banco

A aplicação utiliza a variável de ambiente `DATABASE_URL` para estabelecer a conexão com o PostgreSQL.

Configure essa variável com os dados da sua própria instalação, sem publicar credenciais no repositório.

Antes de executar scripts de carga, verifique seus efeitos. O script `scripts/01_carregar_staging.py` utiliza `if_exists="replace"` no primeiro lote e pode substituir a tabela `staging.material_original`.

**Não execute esse script sobre uma base existente sem avaliar o impacto e garantir que os dados necessários estejam preservados.**

## 10. Execução da aplicação

Com o ambiente virtual ativo, o PostgreSQL disponível e a variável `DATABASE_URL` configurada, execute:

```powershell
python app.py
```

O programa solicita o nome ou parte do nome de um material, apresenta as descrições encontradas e permite selecionar uma delas para consultar os preços.

A aplicação apresenta as estatísticas do grupo selecionado, os limites calculados pelo IQR e as ofertas mais baratas encontradas.

A quantidade máxima de ofertas exibidas é 20. Essa limitação da listagem não significa que os cálculos estatísticos considerem somente essas 20 ofertas.

## 11. Organização e reprodução do processamento

O projeto utiliza os schemas `staging` e `core` para separar os dados originais dos dados organizados para análise.

A reprodução integral do processamento desde o arquivo original até as tabelas relacionais ainda precisa ser verificada, incluindo a sequência de execução dos scripts, as transformações aplicadas e as dependências entre as etapas.

A utilização de schemas distintos no PostgreSQL organiza os dados, mas não caracteriza, por si só, uma arquitetura de banco de dados distribuído.

Caso a disciplina exija recursos de dados semiestruturados ou de distribuição de dados, será necessário verificar o enunciado e comprovar quais recursos foram efetivamente implementados.

## 12. Estado atual do projeto

O projeto possui dados carregados no PostgreSQL, estruturas relacionais, consultas SQL, investigações de qualidade documentadas e uma aplicação de console para comparação de preços.

A aplicação já foi testada com diferentes materiais, incluindo casos com várias ofertas e casos com amostras insuficientes para a classificação estatística.

As próximas atividades de documentação e validação são:

1. Conferir as chaves primárias e estrangeiras das tabelas.
2. Documentar os relacionamentos do modelo relacional.
3. Conferir as transformações executadas na carga dos dados.
4. Verificar a sequência necessária para reproduzir o processamento.
5. Conferir os requisitos da disciplina relacionados a dados semiestruturados e bancos de dados distribuídos.
6. Revisar as instruções de instalação e execução em um ambiente limpo.

## 13. Cuidados

* Não versionar credenciais ou senhas.
* Preservar os arquivos originais sem alterações.
* Não executar scripts de carga sem verificar seus efeitos.
* Documentar as alterações e decisões de tratamento.
* Interpretar comparações de preços considerando as limitações dos dados disponíveis.
* Não tratar automaticamente valores estatisticamente atípicos como erros ou irregularidades.
