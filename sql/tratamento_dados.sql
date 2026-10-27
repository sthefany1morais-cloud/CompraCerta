
-- Projeto: CompraCerta
-- Objetivo: registrar os tratamentos de qualidade aplicados aos dados.
-- Tabela tratada: core.item_compra
-- Tabela staging preservada: staging.material_original
--
-- Tratamentos realizados e confirmados:
-- 1. Remoção de espaços no início e no fim de marca.
-- 2. Conversão de marcas compostas apenas por espaços em NULL.
-- 3. Remoção de espaços no início e no fim de descricao_item.
-- 4. Remoção de espaços no início e no fim de nome_fornecedor.
-- 5. Conversão de criterios_julgamento compostos apenas por espaços em NULL.
--
-- Resultado da validação:
-- Total de registros: 100957
-- Marcas nulas: 36
-- Critérios de julgamento nulos: 15
-- Espaços extras nas colunas tratadas: 0
--
-- IMPORTANTE:
-- Este arquivo documenta os tratamentos já executados.
-- Não execute novamente os comandos de atualização sem necessidade.

-- 1. Verificar marcas com espaços extras
SELECT COUNT(*) AS marcas_com_espacos_extras
FROM core.item_compra
WHERE marca IS NOT NULL
  AND marca <> BTRIM(marca);

-- 2. Verificar descrições com espaços extras
SELECT COUNT(*) AS descricoes_com_espacos_extras
FROM core.item_compra
WHERE descricao_item IS NOT NULL
  AND descricao_item <> BTRIM(descricao_item);

-- 3. Verificar nomes de fornecedores com espaços extras
SELECT COUNT(*) AS fornecedores_com_espacos_extras
FROM core.item_compra
WHERE nome_fornecedor IS NOT NULL
  AND nome_fornecedor <> BTRIM(nome_fornecedor);

-- 4. Verificar critérios contendo apenas espaços
SELECT COUNT(*) AS criterios_com_apenas_espacos
FROM core.item_compra
WHERE criterio_julgamento IS NOT NULL
  AND BTRIM(criterio_julgamento) = '';

-- 5. Verificar o total de registros
SELECT COUNT(*) AS total_registros
FROM core.item_compra;

-- Tratamento: preenchimento de nomes de unidades de fornecimento.
-- Os nomes foram inferidos a partir de correspondências unicas
-- entre siglas e nomes encontrados nos dados originais.
-- Registros sem correspondencia unica permaneceram sem preenchimento.
-- Validar as correspondencias com uma fonte oficial quando disponivel.

SELECT
    COUNT(*) AS total_registros,
    COUNT(*) FILTER (
        WHERE NULLIF(BTRIM(nome_unidade_fornecimento), '') IS NOT NULL
    ) AS nomes_preenchidos,
    COUNT(*) FILTER (
        WHERE NULLIF(BTRIM(nome_unidade_fornecimento), '') IS NULL
    ) AS nomes_ainda_vazios
FROM core.item_compra;



