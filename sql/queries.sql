-- CompraCerta
-- Consultas de analise para o banco compra_certa.
-- Execute cada consulta individualmente no pgAdmin quando precisar dos resultados.

-- 1. Quantidade de registros nas tabelas principais
SELECT 'compra' AS tabela, COUNT(*) AS total FROM core.compra
UNION ALL
SELECT 'item_compra', COUNT(*) FROM core.item_compra
UNION ALL
SELECT 'fornecedor', COUNT(*) FROM core.fornecedor
UNION ALL
SELECT 'catalogo_item', COUNT(*) FROM core.catalogo_item
UNION ALL
SELECT 'orgao', COUNT(*) FROM core.orgao
UNION ALL
SELECT 'localidade', COUNT(*) FROM core.localidade
UNION ALL
SELECT 'unidade_compradora', COUNT(*) FROM core.unidade_compradora
ORDER BY tabela;

-- 2. Estatisticas basicas dos precos unitarios
SELECT
COUNT(*) AS total_itens,
COUNT(preco_unitario) AS itens_com_preco,
MIN(preco_unitario) AS menor_preco,
MAX(preco_unitario) AS maior_preco,
ROUND(AVG(preco_unitario), 2) AS preco_medio
FROM core.item_compra;

-- 3. Quantidade de valores ausentes em campos importantes
SELECT
COUNT(*) FILTER (WHERE preco_unitario IS NULL) AS preco_ausente,
COUNT(*) FILTER (WHERE quantidade IS NULL) AS quantidade_ausente,
COUNT(*) FILTER (WHERE descricao_item IS NULL) AS descricao_ausente,
COUNT(*) FILTER (WHERE id_fornecedor IS NULL) AS fornecedor_ausente,
COUNT(*) FILTER (WHERE id_catalogo_item IS NULL) AS catalogo_ausente
FROM core.item_compra;

-- 4. Dez itens com maior preco unitario
SELECT
id_item_compra,
descricao_item,
preco_unitario,
quantidade,
nome_fornecedor
FROM core.item_compra
WHERE preco_unitario IS NOT NULL
ORDER BY preco_unitario DESC
LIMIT 10;

-- 5. Quantidade de itens por criterio de julgamento
SELECT
criterio_julgamento,
COUNT(*) AS total_itens
FROM core.item_compra
GROUP BY criterio_julgamento
ORDER BY total_itens DESC;

-- 6. Quantidade de itens por estado
SELECT
l.estado,
COUNT(*) AS total_itens
FROM core.item_compra AS i
JOIN core.compra AS c
ON c.id_compra = i.id_compra
JOIN core.unidade_compradora AS u
ON u.id_unidade_compradora = (
SELECT u2.id_unidade_compradora
FROM core.unidade_compradora AS u2
WHERE u2.id_orgao IS NOT NULL
LIMIT 1
)
JOIN core.localidade AS l
ON l.id_localidade = u.id_localidade
GROUP BY l.estado
ORDER BY total_itens DESC;
