-- CompraCerta
-- Documentacao da estrutura existente no PostgreSQL.
-- Arquivo informativo: nao cria nem altera objetos no banco.

-- Schema staging:
--   staging.material_original (42 colunas, todas text)

-- Schema core:
--   core.compra
--   core.item_compra
--   core.fornecedor
--   core.catalogo_item
--   core.orgao
--   core.localidade
--   core.unidade_compradora

-- Relacionamentos identificados:
--   core.item_compra.id_compra
--       -> core.compra.id_compra
--   core.item_compra.id_fornecedor
--       -> core.fornecedor.id_fornecedor
--   core.item_compra.id_catalogo_item
--       -> core.catalogo_item.id_catalogo_item
--   core.unidade_compradora.id_orgao
--       -> core.orgao.id_orgao
--   core.unidade_compradora.id_localidade
--       -> core.localidade.id_localidade

-- Consulta para inspecionar a estrutura real:
-- SELECT table_schema, table_name, column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_schema IN ('staging', 'core')
-- ORDER BY table_schema, table_name, ordinal_position;
