# CompraCerta — Relatório de Qualidade dos Dados

## 1. Fonte e dimensão

- Fonte: Portal de Dados Abertos do Compras.gov.br.
- Arquivo: `material_2026_09.csv`.
- Registros analisados: 100.957.
- Colunas: 42.
- Duplicatas exatas identificadas na inspeção inicial: 0.

## 2. Identificadores e possíveis relacionamentos

- `id_item_compra`: 100.957 valores distintos. Candidato a chave primária; a ausência de valores nulos deve ser validada.
- `id_compra`: 8.208 compras distintas. Um mesmo identificador aparece em vários registros.
- `id_compra_item`: 99.446 valores distintos. Foram encontradas 2.960 linhas com identificadores repetidos, distribuídas por 1.449 identificadores.
- Os exemplos analisados indicam que um item de compra pode estar associado a fornecedores diferentes. Os registros repetidos não serão excluídos sem validação.

## 3. Inconsistências e ausências

- O campo `estado` contém o valor `EX`, associado à Comissão Naval Brasileira em Washington. O valor será preservado e documentado como localização no exterior, sem conversão para uma UF brasileira.
- Foram identificados códigos de órgão associados a nomes diferentes e uma UASG associada a duas descrições. Os nomes originais serão preservados; a padronização dependerá de validação.
- Foram encontrados quatro registros com `preco_unitario = 0` e `quantidade = 0`, todos associados à mesma compra e ao mesmo fornecedor. Esses registros serão marcados para investigação, não excluídos automaticamente.
- `nome_unidade_medida` está ausente em todos os registros.
- `sigla_unidade_medida`, `nome_unidade_fornecimento`, `sigla_unidade_fornecimento`, `municipio`, `codigo_municipio`, `poder`, `marca` e `criterio_julgamento` também apresentam valores ausentes em diferentes proporções.

## 4. Regras iniciais de tratamento

1. Preservar o arquivo de origem e seus valores originais.
2. Manter identificadores e códigos como texto quando necessário para preservar zeros à esquerda.
3. Não excluir registros apenas porque identificadores de negócio se repetem.
4. Não substituir valores ausentes por valores inventados.
5. Não converter automaticamente preços ou quantidades iguais a zero em valores ausentes.
6. Manter os nomes originais de órgãos e unidades em uma camada de origem e documentar futuras padronizações.
7. Criar tabelas relacionais somente após validar chaves e relacionamentos.

## 5. Próximas verificações

- Confirmar se `id_item_compra` é único e não nulo em todo o conjunto.
- Investigar os quatro registros com preço e quantidade iguais a zero.
- Validar os códigos de órgão e UASG com descrições divergentes.
- Carregar os dados originais em uma área de preparação do PostgreSQL.
- Construir o modelo relacional normalizado a partir dos relacionamentos verificados.