# CompraCerta — Relatório de Qualidade dos Dados

## 1. Fonte e dimensão

* **Fonte:** Portal de Dados Abertos do Compras.gov.br.
* **Arquivo:** `material_2026_09.csv`.
* **Registros analisados:** 100.957.
* **Colunas na fonte original:** 42.
* **Duplicatas exatas identificadas na inspeção inicial:** 0.

## 2. Identificadores e possíveis relacionamentos

* `id_item_compra`: 100.957 valores distintos e não nulos na tabela de origem e na tabela `core.item_compra`.
* `id_compra`: 8.208 compras distintas. Uma compra pode estar associada a vários itens.
* `id_compra_item`: 99.446 valores distintos. Foram encontradas 2.960 linhas com identificadores repetidos, distribuídas por 1.449 identificadores.
* Os exemplos analisados indicam que um identificador de item de compra pode aparecer em registros associados a fornecedores diferentes. Esses registros são preservados, sem exclusão automática.
* Os relacionamentos entre itens, compras, fornecedores e catálogo foram implementados por meio de chaves estrangeiras.

## 3. Estrutura do banco de dados

O banco PostgreSQL `compra_certa` possui os esquemas `staging` e `core`.

A tabela `staging.material_original` mantém 100.957 registros da fonte original.

O esquema `core` possui as seguintes tabelas:

| Tabela               | Registros |
| -------------------- | --------: |
| `compra`             |     8.208 |
| `item_compra`        |   100.957 |
| `fornecedor`         |    10.873 |
| `orgao`              |     1.108 |
| `localidade`         |       632 |
| `unidade_compradora` |     2.414 |
| `catalogo_item`      |    39.008 |

Foram verificadas cinco chaves estrangeiras:

* `item_compra.id_compra` → `compra.id_compra`
* `item_compra.id_fornecedor` → `fornecedor.id_fornecedor`
* `item_compra.id_catalogo_item` → `catalogo_item.id_catalogo_item`
* `unidade_compradora.id_orgao` → `orgao.id_orgao`
* `unidade_compradora.id_localidade` → `localidade.id_localidade`

Na tabela `core.item_compra`, os 100.957 registros possuem `id_fornecedor` e `id_catalogo_item` preenchidos. As duas colunas foram definidas como obrigatórias (`NOT NULL`) e possuem chaves estrangeiras.

## 4. Inconsistências e ausências identificadas

* O campo `estado` contém o valor `EX`, associado à Comissão Naval Brasileira em Washington. O valor é preservado como indicação de localização no exterior, sem conversão para uma UF brasileira.
* Foram identificados códigos de órgão associados a nomes diferentes e um código de UASG associado a descrições divergentes. Os nomes originais são preservados até que a padronização possa ser validada.
* Foram encontrados quatro registros com `preco_unitario = 0` e `quantidade = 0`, associados à mesma compra e ao mesmo fornecedor. Esses registros devem ser investigados, sem exclusão automática.
* `nome_unidade_medida` está ausente em todos os registros da fonte analisada.
* `sigla_unidade_medida`, `nome_unidade_fornecimento`, `sigla_unidade_fornecimento`, `municipio`, `codigo_municipio`, `poder`, `marca` e `criterio_julgamento` também apresentam ausências em diferentes proporções.
* Foram identificadas 12 unidades compradoras sem associação com um registro de `core.localidade`. Os dados disponíveis não permitem determinar a localidade com segurança.

## 5. Regras de tratamento

1. Preservar os dados originais na camada de preparação.
2. Manter identificadores e códigos como texto quando necessário para preservar zeros à esquerda.
3. Não excluir registros apenas porque identificadores de negócio se repetem.
4. Não substituir valores ausentes por valores inventados.
5. Não converter automaticamente preços ou quantidades iguais a zero em valores ausentes.
6. Preservar os nomes originais de órgãos e unidades compradoras e documentar divergências antes de padronizá-los.
7. Criar relacionamentos no modelo relacional somente após validar as chaves e as correspondências.
8. Manter `id_localidade` como `NULL` quando não houver evidência suficiente para determinar a localidade.
9. Preservar o valor `EX`, sem tratá-lo como uma UF brasileira.
10. Investigar valores suspeitos antes de decidir por correção, exclusão ou exclusão de análises específicas.

## 6. Verificações concluídas

* Confirmada a unicidade e o preenchimento de `id_item_compra` nos 100.957 registros analisados.
* Confirmados 100.957 registros em `core.item_compra`.
* Confirmado que os 100.957 itens possuem fornecedor e item de catálogo associados.
* Verificada a existência das cinco chaves estrangeiras do esquema `core`.
* Contabilizados os registros das sete tabelas principais.
* Realizado backup do banco de dados antes das alterações recentes no modelo.

## 7. Pendências

* Investigar os quatro registros com preço e quantidade iguais a zero.
* Validar os códigos de órgão e UASG com descrições divergentes.
* Avaliar valores extremos de preços antes de utilizá-los em comparações.
* Investigar possibilidades de associação das 12 unidades compradoras sem localidade, sem inferir informações sem evidência suficiente.
* Revisar os códigos de classificação e julgamento com base em documentação oficial.
* Desenvolver e testar o processo de tratamento dos dados para que possa ser reproduzido.
* Implementar as funcionalidades de comparação de preços do CompraCerta.
