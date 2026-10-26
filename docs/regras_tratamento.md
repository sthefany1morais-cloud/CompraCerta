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

## 6. Localidades

* Preservar o valor `EX` no campo `estado`, pois representa uma localização no exterior no conjunto analisado.
* Não converter `EX` em uma unidade federativa brasileira.
* Não preencher municípios ausentes com base apenas em suposições derivadas do nome da unidade compradora.

## 7. Integridade relacional

As verificações realizadas não identificaram itens sem correspondência em compras, fornecedores ou catálogo, nem unidades compradoras sem correspondência em órgãos.

Antes de adicionar novas chaves estrangeiras ao modelo relacional, validar as correspondências e a cardinalidade das relações.

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
