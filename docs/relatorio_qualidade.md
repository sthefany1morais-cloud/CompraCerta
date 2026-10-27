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
* Foram identificados seis itens com preços unitários potencialmente atípicos em uma mesma compra, realizada em 10/09/2026. Os valores variam de R$ 1.800.000,00 a R$ 95.929.000,00, todos com quantidade registrada igual a 1.
* A compra está associada ao fornecedor MPF Comércio e Representação de Produtos Hospitalares Ltda., CNPJ `46878679000117`, e ao identificador `92962105000012026`.
* Entre os itens analisados estão um dispositivo plástico para alívio da dor associada a injeções, um monitor multiparâmetro, um conjunto para prótese dental, uma mesa auxiliar hospitalar, um motor odontológico e um rodízio para mocho.
* A comparação entre `staging.material_original` e `core.item_compra` confirmou que os preços desses seis itens são iguais nas duas tabelas. Portanto, os valores não foram introduzidos pelo processo de tratamento.
* Os valores são considerados **possíveis anomalias de preço**, e não erros confirmados. Ainda é necessário consultar documentação adicional para verificar se decorrem de erros de registro, problemas de unidade de medida ou outra situação.
* A investigação confirmou seis códigos de órgão com nomes divergentes (`15000`, `22203`, `29208`, `30202`, `94268` e `95571`). Os diferentes nomes também aparecem na fonte original e podem refletir abreviações, diferenças de formatação ou mudanças de denominação institucional.
* Foi identificado o código UASG `981981`, associado aos nomes `MPB - PREFEITURA MUNICIPAL DE CAMPINA GRANDE` e `PREFEITURA MUNICIPAL DE CAMPINA GRANDE - PB`. Ambos aparecem na fonte original e parecem se referir à mesma instituição.
* As divergências foram preservadas. Qualquer padronização deverá utilizar regras documentadas e, quando necessário, validação por fonte oficial, sem sobrescrever os dados originais.
* A investigação das 12 unidades compradoras sem associação com `core.localidade` confirmou que os campos `municipio` e `codigo_municipio` também estão ausentes na fonte original para todos esses registros. O campo `estado` está preenchido em 11 casos; a unidade correspondente à Comissão Naval Brasileira em Washington apresenta o valor `EX`. Como não há evidência suficiente para determinar os municípios e seus códigos, os registros permanecem sem associação de localidade, sem preenchimento por inferência.

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
11. Preservar os preços potencialmente atípicos nas tabelas originais e tratadas até que sua validade seja investigada.
12. Documentar a diferença entre valores atípicos identificados e erros efetivamente confirmados.
13. Quando necessário, excluir valores suspeitos de análises comparativas específicas apenas mediante critérios documentados, sem apagar os registros da base.

## 6. Verificações concluídas

* Confirmada a unicidade e o preenchimento de `id_item_compra` nos 100.957 registros analisados.
* Confirmados 100.957 registros em `core.item_compra`.
* Confirmado que os 100.957 itens possuem fornecedor e item de catálogo associados.
* Verificada a existência das cinco chaves estrangeiras do esquema `core`.
* Contabilizados os registros das sete tabelas principais.
* Realizado backup do banco de dados antes das alterações recentes no modelo.
* Comparados os preços dos seis itens potencialmente atípicos entre as tabelas `staging.material_original` e `core.item_compra`, sem diferenças nos valores observados.

## 7. Pendências

* Investigar os quatro registros com preço e quantidade iguais a zero.
* Validar os códigos de órgão e UASG com descrições divergentes.
* Investigar os seis preços potencialmente atípicos e consultar documentação adicional da compra.
* Avaliar outros valores extremos de preços antes de utilizá-los em comparações.
* Investigar possibilidades de associação das 12 unidades compradoras sem localidade, sem inferir informações sem evidência suficiente.
* Revisar os códigos de classificação e julgamento com base em documentação oficial.
* Desenvolver e testar o processo de tratamento dos dados para que possa ser reproduzido.
* Implementar as funcionalidades de comparação de preços do CompraCerta.

### 8. Critérios de julgamento

A coluna `criterio_julgamento`, da tabela `staging.material_original`, apresenta seis valores distintos: `0`, `1`, `2`, `V`, `D` e registros em branco.

Foram identificados 15 registros com valores compostos apenas por espaços, que devem ser tratados como valores ausentes, preservando-se os dados originais.

A análise do campo `percentual_maior_desconto` identificou os seguintes padrões:

* O código `0` aparece em 15.552 registros, todos com percentual de desconto igual a zero.
* O código `V` aparece em 33.628 registros, todos com percentual de desconto igual a zero.
* O código `D` aparece em 70 registros, todos com percentuais de desconto preenchidos e variados.

Essas associações são evidências exploratórias, mas não confirmam, por si só, o significado oficial dos códigos. Até que a documentação oficial seja validada, os valores devem ser preservados sem substituições ou classificações presumidas. Os 15 registros em branco devem ser identificados como ausentes nas análises.

**Pendência:** confirmar o significado dos códigos `0`, `1`, `2`, `V` e `D` em documentação oficial do Compras.gov.br e registrar as regras de tratamento correspondentes.

### 9. Análise das unidades de medida

Foram analisados os campos `sigla_unidade_medida` e `nome_unidade_medida` da tabela `core.item_compra`, que contém 100.957 registros.

Os resultados identificaram:

* 85.328 registros sem sigla de unidade de medida;
* 100.957 registros sem nome de unidade de medida.

A investigação na tabela de origem `staging.material_original` confirmou que os nomes das unidades de medida também estão ausentes na fonte original. Embora existam siglas preenchidas em parte dos registros, não foi identificada uma referência confiável que permita reconstruir os nomes com segurança.

**Decisão de tratamento:** os valores ausentes foram mantidos, sem preenchimento por suposição. O preenchimento futuro depende de uma fonte de referência confiável para validar as correspondências entre siglas e nomes.

### 10. Investigação de identificadores repetidos de fornecedores

Durante a análise da tabela `core.fornecedor`, foram identificados 10.873 registros e 10.757 identificadores distintos, indicando a existência de identificadores repetidos.

A investigação na fonte original `staging.material_original` identificou três valores associados a múltiplos fornecedores diferentes:

* **`000000000`:** associado a sete nomes distintos de fornecedores.
* **`ESTRANGEIRO`:** associado a três nomes distintos de fornecedores.
* **`TMA6748F62`:** associado a quatro nomes distintos de fornecedores.

Esses resultados indicam que os valores investigados não identificam individualmente todos os fornecedores aos quais estão associados. A presença desses valores também foi confirmada na fonte original, portanto não há evidência de que tenham sido criados pelo tratamento dos dados.

**Decisão de tratamento:** os registros foram preservados, sem exclusão ou criação de identificadores artificiais. A correção desses casos depende de uma fonte de referência confiável que permita identificar individualmente os fornecedores.

### 11. Verificação das datas de compra e atualização

A tabela `core.compra` foi analisada para verificar a relação entre `data_compra` e `data_hora_atualizacao_compra`.

Os resultados foram:

* **Registros analisados:** 8.208.
* **Atualizações anteriores à data da compra:** 0.
* **Atualizações no mesmo dia da compra:** 0.
* **Atualizações posteriores à data da compra:** 8.208.
* **Menor intervalo entre compra e atualização:** 1 dia.
* **Maior intervalo:** 39 dias.
* **Intervalo médio:** 8,77 dias.

**Conclusão:** todas as atualizações ocorreram depois da data da compra, com intervalos de 1 a 39 dias. Esses resultados, isoladamente, não indicam erros. Os registros foram preservados, sem alterações.

### 12. Divergências nos identificadores de fornecedores

Foi realizada uma análise dos identificadores dos fornecedores na tabela `core.fornecedor`.

Foram identificados 10.309 registros com identificadores numéricos de 14 dígitos, 457 com identificadores numéricos de 11 dígitos, 14 com identificadores numéricos de outros tamanhos e 93 com identificadores alfanuméricos.

Entre os identificadores numéricos de 14 dígitos, foram encontrados 104 identificadores associados a nomes distintos, envolvendo 208 registros. A verificação na tabela de origem `staging.material_original` confirmou que essas divergências já estavam presentes nos dados originais.

As diferenças incluem variações de grafia, abreviações e nomes empresariais distintos associados ao mesmo identificador. Não foi possível determinar, apenas com os dados disponíveis, qual nome deve ser considerado correto em cada caso.

Também foram observados identificadores genéricos, como `000000000` e `ESTRANGEIRO`, além de identificadores alfanuméricos e numéricos com tamanhos diferentes dos formatos de CPF e CNPJ.

**Decisão de tratamento:** os identificadores e nomes originais foram preservados. Não foram realizadas unificações automáticas de fornecedores, alterações de identificadores ou exclusões de registros. Os casos identificados permanecem como pontos de atenção para eventual validação com uma fonte cadastral confiável.
