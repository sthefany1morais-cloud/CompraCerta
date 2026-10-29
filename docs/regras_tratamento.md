# CompraCerta — Regras de Tratamento dos Dados

## 1. Objetivo

Documentar as regras de limpeza, padronização e validação dos dados de compras públicas utilizados no CompraCerta.

Os dados originais devem ser preservados. As transformações serão aplicadas em uma camada separada, permitindo rastreabilidade e comparação dos resultados antes e depois do tratamento.

## 2. Identificadores e duplicidades

* Manter `id_item_compra` como identificador do item, pois foram confirmados 100.957 valores não nulos e distintos em 100.957 registros de `core.item_compra`.
* Não excluir registros apenas porque `id_compra_item` se repete.
* Investigar possíveis duplicidades completas antes de decidir pela remoção de qualquer registro.
* Preservar códigos e identificadores como texto quando necessário para evitar perda de zeros à esquerda.

## 3. Valores ausentes

* Converter valores compostos somente por espaços em `NULL` na camada tratada.
* Não inventar valores para campos ausentes.
* Preservar os valores originais na camada `staging`.
* O campo `nome_unidade_medida` está ausente em todos os registros e deverá ser documentado como limitação da fonte.
* Os 12 registros de unidades compradoras sem localidade associada permanecerão pendentes até que exista informação confiável para preenchê-los.

## 4. Preços e quantidades

* Não excluir automaticamente registros com preço ou quantidade iguais a zero.
* Investigar os quatro registros que apresentam simultaneamente `preco_unitario = 0` e `quantidade = 0`.
* Sinalizar valores suspeitos para que não distorçam comparações de preços.
* Investigar valores extremos antes de classificá-los como erros.
* Não substituir valores suspeitos por estimativas sem justificativa documentada.

## 5. Órgãos e unidades compradoras

* Preservar os nomes originais na camada de origem.
* Investigar códigos de órgão associados a diferentes nomes antes de padronizar.
* Investigar a divergência de nomes identificada para a unidade compradora de código `981981`.
* Não presumir que nomes diferentes representem instituições distintas, nem que representem a mesma instituição, sem validação.

### 5.1 Validação dos códigos UASG

A comparação entre `staging.material_original` e `core.unidade_compradora` identificou 2.413 códigos UASG distintos na fonte original e a mesma quantidade na tabela tratada. Todos os códigos da fonte possuem correspondência na tabela `core.unidade_compradora`.

A tabela tratada contém 2.414 registros, correspondentes a 2.413 códigos distintos. A diferença decorre do código UASG `981981`, que aparece em dois registros com nomes diferentes:

* `MPB - PREFEITURA MUNICIPAL DE CAMPINA GRANDE`
* `PREFEITURA MUNICIPAL DE CAMPINA GRANDE - PB`

Os dois registros são preservados, sem exclusão ou unificação automática, pois a diferença de nome, isoladamente, não é suficiente para justificar uma alteração nos dados.

## 6. Localidades

* Preservar o valor `EX` no campo `estado`, pois representa uma localização no exterior no conjunto analisado.
* Não converter `EX` em uma unidade federativa brasileira.
* Não preencher municípios ausentes com base apenas em suposições derivadas do nome da unidade compradora.

## 7. Integridade relacional

As verificações realizadas não identificaram itens sem correspondência em compras, fornecedores ou catálogo, nem unidades compradoras sem correspondência em órgãos.

Antes de adicionar novas chaves estrangeiras ao modelo relacional, validar as correspondências e a cardinalidade das relações.

### 7.1 Resultado da validação no PostgreSQL

Foram executadas consultas para verificar a existência de registros sem correspondência nas tabelas relacionadas. Os resultados foram:

| Verificação                                                                    | Registros sem correspondência |
| ------------------------------------------------------------------------------ | ----------------------------: |
| Itens de compra sem material no catálogo                                       |                             0 |
| Itens de compra sem fornecedor                                                 |                             0 |
| Itens de compra sem compra correspondente                                      |                             0 |
| Sinônimos sem material no catálogo                                             |                             0 |
| Unidades compradoras sem órgão correspondente, considerando IDs não nulos      |                             0 |
| Unidades compradoras sem localidade correspondente, considerando IDs não nulos |                             0 |

As verificações não identificaram registros órfãos nos relacionamentos analisados.

A ausência de correspondência não foi confundida com valores nulos: unidades compradoras sem localidade informada continuam sujeitas às regras específicas de tratamento descritas neste documento.

## 8. Validação após o tratamento

Após implementar as regras, comparar os dados antes e depois do tratamento, registrando:

* Quantidade total de registros.
* Quantidade de identificadores distintos e valores nulos.
* Quantidade de valores ausentes por campo.
* Quantidade de registros sinalizados por preço ou quantidade suspeitos.
* Quantidade de registros sem correspondência nas relações.
* Alterações de padronização aplicadas.

## 9. Princípio geral

Nenhum registro deverá ser excluído ou ter seu significado alterado sem uma regra explícita, justificativa e validação dos resultados.

### 10. Pendências de localidade

Foram identificadas 12 unidades compradoras sem associação com um registro da tabela `core.localidade`. Na fonte original,
esses registros não apresentam informações suficientes de município e código municipal para estabelecer uma associação segura.

**Regra de tratamento:**

* Manter `id_localidade` como `NULL` até que exista uma fonte confiável para confirmar a localidade.
* Preservar os dados originais das unidades compradoras.
* Não criar localidades fictícias nem inferir municípios sem evidência suficiente.
* Preservar o estado `EX` para unidades localizadas no exterior, sem convertê-lo para uma UF brasileira.

Esses registros devem permanecer documentados como pendências de qualidade dos dados.

### 11. Tratamento de preços zerados

Foram identificados quatro registros com `preco_unitario = 0` e `quantidade = 0` na base analisada. Todos pertencem à mesma compra e ao mesmo fornecedor.

**Regra de tratamento:**

* Preservar os quatro registros no banco de dados.
* Não substituir os valores por preços estimados.
* Excluir esses registros dos cálculos de comparação de preços, identificando-os como não elegíveis para essa análise.
* Manter os valores originais disponíveis para auditoria e investigações futuras.

Essa regra evita que valores zerados distorçam os resultados da comparação de preços sem eliminar informações da fonte original.

### 12. Importação dos dados originais

A importação dos dados é realizada pelo script `scripts/01_carregar_staging.py`, que localiza um arquivo CSV no diretório `data/raw/extraido` e utiliza a biblioteca pandas para ler seu conteúdo.

Os dados são carregados com os campos inicialmente tratados como texto, por meio do parâmetro `dtype=str`. O separador é detectado automaticamente durante a leitura.

Para controlar o consumo de memória, a leitura é realizada em lotes de até 10.000 linhas. A gravação no PostgreSQL utiliza lotes de até 1.000 registros.

Os dados são armazenados na tabela `staging.material_original`, no schema `staging` do banco `compra_certa`. Na primeira gravação, a tabela é substituída; nas gravações seguintes, os registros são acrescentados.

Como a primeira gravação pode substituir uma tabela existente, o script deve ser executado somente após a verificação do arquivo de entrada e dos efeitos da operação sobre os dados armazenados.

### 13. Inspeção inicial dos dados

A inspeção inicial é realizada pelo script `scripts/02_inspecionar.py`. O procedimento utiliza o arquivo compactado `data/raw/material_2026_09.csv.zip` e extrai seu conteúdo para o diretório `data/raw/extraido`, preservando o arquivo ZIP original.

Após a extração, o script verifica se existe pelo menos um arquivo CSV no diretório de destino. Em seguida, lê o arquivo selecionado com a biblioteca pandas, mantendo as colunas como texto por meio de `dtype=str` e utilizando a detecção automática do separador.

A inspeção contempla as dimensões do conjunto de dados, os nomes das colunas, as informações de tipos e preenchimento, os cinco primeiros registros, a quantidade de valores nulos por coluna e a contagem de linhas completamente duplicadas.

O parâmetro `on_bad_lines="error"` determina que a leitura gere um erro quando forem identificadas linhas malformadas pelo mecanismo de leitura utilizado.

Essa etapa tem finalidade diagnóstica. Ela permite conhecer a estrutura dos dados e identificar possíveis problemas que deverão ser investigados nas etapas seguintes, mas não realiza limpeza, correção ou exclusão de registros.

### 14. Análise da qualidade dos dados

A análise da qualidade é realizada pelo script `scripts/03_qualidade.py`, que lê o arquivo CSV extraído e calcula indicadores descritivos para cada coluna.

O relatório inclui o tipo de dado identificado pelo pandas, a quantidade e o percentual de valores ausentes e a quantidade de valores distintos, desconsiderando os valores ausentes na contagem de distintos.

O script também contabiliza as linhas completamente duplicadas e apresenta os resultados no terminal.

Os indicadores são exportados para `data/processed/relatorio_qualidade.csv`, utilizando codificação UTF-8. O diretório de destino é criado automaticamente caso não exista.

Essa etapa tem finalidade diagnóstica. O relatório apoia a investigação e a documentação dos problemas encontrados, mas não realiza automaticamente a limpeza ou a exclusão de registros.

### 15. Investigação de inconsistências

O script `scripts/04_investigar.py` realiza verificações direcionadas para identificar possíveis problemas nos dados originais.

Inicialmente, os nomes das colunas são tratados para remover o caractere BOM, espaços externos e aspas extras. Em seguida, o script apresenta as dimensões do conjunto de dados e os nomes das colunas.

A investigação contempla a distribuição de valores em campos categóricos, a repetição de valores em identificadores e a relação entre códigos e nomes de municípios.

Nos campos categóricos, são apresentados até 40 valores por coluna, incluindo valores ausentes. Nos identificadores, são exibidas a quantidade de linhas, a quantidade de valores distintos e a quantidade de linhas com valores repetidos.

Quando as colunas de código e nome do município estão disponíveis, o script identifica quantos nomes distintos aparecem associados a cada código.

Por fim, são exportadas até 1.000 linhas para `data/processed/amostra_inspecao.csv`, permitindo consultas e investigações posteriores.

Essas verificações são diagnósticas. A repetição de identificadores ou a existência de múltiplos nomes associados a um código não comprova, isoladamente, a existência de um erro. Os resultados precisam ser analisados considerando o significado de cada campo e as regras do conjunto de dados.

### 16. Investigação detalhada dos dados

O script `scripts/05_investigar_detalhado.py` realiza verificações específicas para aprofundar a investigação de possíveis inconsistências nos registros.

Inicialmente, padroniza os nomes das colunas, removendo caracteres BOM, espaços externos e aspas extras. Em seguida, converte strings vazias ou compostas apenas por espaços em valores ausentes.

A análise contempla os registros com estado igual a `EX`, a repetição do identificador `id_compra_item`, a presença de valores ausentes ou não numéricos, valores negativos e valores iguais a zero nos campos de preço unitário e quantidade.

O script também identifica os campos com valores ausentes e investiga possíveis conflitos entre códigos e nomes de municípios, órgãos, unidades compradoras, classes, grupos e PDMs, quando as colunas correspondentes estão disponíveis.

Os registros associados a identificadores repetidos são exportados para `data/processed/id_compra_item_repetidos.csv`, permitindo sua análise posterior.

Essa etapa é investigativa e não realiza a exclusão automática de registros. Estados fora do padrão, identificadores repetidos e divergências entre códigos e nomes são tratados como situações que exigem análise contextual antes de qualquer decisão de correção.

### 17. Investigação de conflitos entre registros

O script `scripts/06_investigar_conflitos.py` aprofunda a investigação de possíveis divergências entre códigos e nomes de órgãos e unidades compradoras.

Inicialmente, os cabeçalhos são padronizados e as strings vazias ou compostas apenas por espaços são convertidas em valores ausentes.

Para os órgãos, o script identifica códigos associados a mais de um nome. Para as unidades compradoras, identifica códigos de UASG associados a nomes diferentes e apresenta também as informações dos órgãos correspondentes.

O script também investiga registros com preço unitário igual a zero e registros com quantidade igual a zero, exibindo informações que permitem analisar cada ocorrência.

Os resultados são apresentados no terminal. Essa etapa não realiza correções automáticas nem exclui registros. As ocorrências identificadas devem ser avaliadas considerando o contexto dos dados e as evidências disponíveis.

## 18. Aplicação de comparação de preços (`app.py`)

A aplicação permite pesquisar materiais cadastrados no banco de dados e comparar os preços registrados nas compras públicas.

### 18.1. Pesquisa e seleção do material

O usuário informa o nome ou parte da descrição do material. A aplicação pesquisa as descrições existentes em `core.catalogo_item`, apresenta até 30 resultados e permite selecionar o material desejado.

Em seguida, são apresentadas as combinações de unidade de fornecimento, nome da unidade e capacidade, acompanhadas da quantidade de ofertas disponíveis.

### 18.2. Critério de inclusão das ofertas

Para a comparação, são consideradas as ofertas com preço unitário maior que zero e com sigla de unidade de fornecimento informada.

A comparação é realizada separadamente para cada combinação de descrição do material, unidade, nome da unidade e capacidade. Essa separação busca evitar a comparação direta de preços associados a apresentações diferentes.

### 18.3. Estatísticas descritivas

Para cada combinação selecionada, a aplicação calcula:

* total de ofertas;
* menor preço;
* maior preço;
* preço médio;
* mediana dos preços.

Também apresenta a diferença percentual entre a mediana e o menor preço, calculada em relação à mediana.

### 18.4. Identificação estatística de possíveis preços atípicos

A aplicação utiliza o método do intervalo interquartil (IQR). São calculados o primeiro quartil (Q1), o terceiro quartil (Q3) e o intervalo interquartil, correspondente à diferença entre Q3 e Q1.

Os limites estatísticos são definidos por:

* Limite inferior: Q1 − 1,5 × IQR, limitado a zero como valor mínimo.
* Limite superior: Q3 + 1,5 × IQR.

Preços abaixo do limite inferior são classificados como `POSSIVEL PRECO ATIPICO - ABAIXO`. Preços acima do limite superior são classificados como `POSSIVEL PRECO ATIPICO - ACIMA`. Os demais são classificados como `DENTRO DO PADRAO`.

Quando há menos de cinco ofertas, a aplicação informa `AMOSTRA INSUFICIENTE`, sem classificar estatisticamente os preços.

### 18.5. Exibição das ofertas

As ofertas são ordenadas pelo preço unitário em ordem crescente, e a aplicação exibe até 20 registros. São apresentados o fornecedor, o preço unitário, a unidade de fornecimento, a capacidade, a quantidade, a identificação da compra e a classificação estatística.

### 18.6. Interpretação dos resultados

As classificações estatísticas servem como sinais para orientar a investigação dos preços. Um preço identificado como potencialmente atípico não comprova, por si só, erro, sobrepreço, fraude ou irregularidade.

Os resultados devem ser interpretados considerando a quantidade de ofertas, a comparabilidade dos materiais e das unidades, e o contexto de cada compra.

## 19. Relacionamento entre compras e unidades compradoras

A tabela `core.compra` ainda não possui relacionamento direto com `core.unidade_compradora`, embora a fonte original disponibilize o código UASG associado a cada compra.

Na análise dos dados, foram identificadas 8.208 compras. Todas possuem correspondência com unidades compradoras pelo código UASG. Entretanto, 25 compras apresentam correspondência ambígua devido à existência de dois registros para a UASG `981981`.

Os dois registros possuem os mesmos valores para `id_orgao`, `id_localidade`, `poder` e `esfera`, mas apresentam nomes diferentes:

* `MPB - PREFEITURA MUNICIPAL DE CAMPINA GRANDE`
* `PREFEITURA MUNICIPAL DE CAMPINA GRANDE - PB`

A investigação confirmou que as duas variações de nome já existem nos dados originais: uma aparece em 19 compras e a outra em 6 compras.

**Decisão de tratamento:** preservar os registros existentes, documentar a divergência e não excluir dados nem estabelecer associações arbitrárias. A implementação de um relacionamento direto entre compras e unidades compradoras deverá ocorrer somente após a definição e validação de uma regra de associação segura.
