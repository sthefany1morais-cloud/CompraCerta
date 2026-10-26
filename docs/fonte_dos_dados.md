# CompraCerta — Documentação da Fonte de Dados

## 1. Identificação da fonte

* **Portal:** Compras.gov.br — Dados Abertos.
* **Tipo de dado:** pesquisa de preços de materiais de compras públicas.
* **Arquivo original:** `material_2026_09.csv.zip`.
* **Arquivo de dados:** `material_2026_09.csv`.
* **Período de referência:** setembro de 2026, conforme a identificação do arquivo.
* **Formato:** CSV compactado em ZIP.
* **Delimitador, codificação e formato de datas:** devem ser documentados após a confirmação dos parâmetros utilizados na leitura do arquivo.

## 2. Localização da fonte

O arquivo foi obtido no diretório de pesquisa de preços de materiais do Compras.gov.br:

`https://repositorio.dados.gov.br/seges/comprasgov/pesquisa_precos/2026/09/`

Nome do arquivo disponibilizado no diretório:

`material_2026_09.csv.zip`

## 3. Armazenamento no projeto

O arquivo compactado está armazenado em:

`data/raw/material_2026_09.csv.zip`

A cópia extraída dos dados também está presente no projeto.

A pasta `data/raw` deve ser utilizada para preservar os arquivos originais, sem aplicar correções diretamente sobre eles.

## 4. Dimensão dos dados analisados

* Registros na tabela `staging.material_original`: 100.957.
* Colunas na tabela original: 42.
* Registros na tabela `core.item_compra`: 100.957.
* Identificadores `id_item_compra` distintos na tabela `core.item_compra`: 100.957.

## 5. Política de preservação

1. Preservar o arquivo ZIP original.
2. Não modificar diretamente o CSV de origem.
3. Realizar a limpeza em uma camada separada dos dados originais.
4. Registrar as regras de transformação e as decisões tomadas.
5. Não excluir registros suspeitos sem investigação e justificativa.
6. Manter códigos e identificadores como texto quando necessário para preservar seu conteúdo original.
7. Documentar a data de obtenção do arquivo quando ela puder ser confirmada.

## 6. Observação sobre a atualização dos dados

O nome do arquivo indica setembro de 2026. A data exata de publicação ou de download ainda precisa ser confirmada, pois não deve ser inferida apenas pelo nome do arquivo.

Esta documentação registra a origem declarada e o armazenamento dos dados utilizados no projeto CompraCerta.
