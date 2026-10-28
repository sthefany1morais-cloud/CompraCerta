# CompraCerta

Projeto de análise e qualidade de dados de compras públicas, utilizando dados abertos do Compras.gov.br.

## Objetivo

Explorar dados de pesquisa de preços de materiais de compras públicas, avaliar sua qualidade, investigar inconsistências e documentar as decisões de tratamento.

## Fonte de dados

* **Portal:** Compras.gov.br — Dados Abertos
* **Arquivo:** `material_2026_09.csv.zip`
* **Período de referência:** setembro de 2026
* **Formato:** CSV compactado em ZIP
* **Registros analisados:** 100.957
* **Colunas da fonte:** 42

A descrição detalhada da origem está em [`docs/fonte_dos_dados.md`](docs/fonte_dos_dados.md).

## Estrutura do projeto

* `data/raw/`: arquivos originais, preservados sem alterações.
* `data/processed/`: relatórios e arquivos derivados das inspeções.
* `docs/`: documentação da fonte, regras de tratamento e relatório de qualidade.
* `notebooks/`: espaço para análises exploratórias em notebooks.
* `scripts/`: scripts de inspeção, qualidade e investigação.
* `sql/`: scripts SQL relacionados ao banco de dados.
* `src/`: espaço destinado aos módulos da aplicação.
* `requirements.txt`: dependências Python do projeto.

## Tecnologias

* Python
* pandas
* SQLAlchemy
* psycopg
* PostgreSQL

## Configuração do ambiente

Recomenda-se utilizar um ambiente virtual Python.

No terminal, na raiz do projeto, execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se o ambiente virtual já estiver ativo, não é necessário ativá-lo novamente.

## Banco de dados

O projeto utiliza PostgreSQL com o banco `compra_certa` e os schemas `staging` e `core`.

O schema `staging` preserva os dados carregados da fonte. O schema `core` contém as tabelas estruturadas para análise.

O script `scripts/01_carregar_staging.py` utiliza a variável de ambiente `DATABASE_URL` para configurar a conexão. **Atenção:** a carga utiliza `if_exists="replace"` no primeiro lote e pode substituir a tabela `staging.material_original`. Não execute esse script sobre uma base existente sem avaliar o impacto.

## Qualidade dos dados

As verificações e decisões realizadas estão documentadas em:

* [`docs/regras_tratamento.md`](docs/regras_tratamento.md)
* [`docs/relatorio_qualidade.md`](docs/relatorio_qualidade.md)

Os registros suspeitos não devem ser excluídos automaticamente. As decisões precisam considerar a origem, as evidências disponíveis e as regras documentadas.

## Estado do projeto

O projeto já possui dados carregados no PostgreSQL, investigações de qualidade documentadas e scripts de inspeção. A automação completa e a reprodução integral das transformações ainda precisam ser verificadas.

## Cuidados

* Não versionar credenciais ou senhas.
* Preservar os arquivos originais.
* Não executar scripts de carga sem verificar seus efeitos.
* Documentar alterações e decisões de tratamento.

git add README.md