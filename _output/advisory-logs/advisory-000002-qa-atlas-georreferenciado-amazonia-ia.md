# QA Log -- advisory-000002 | 2026-04-24 01:18 UTC | Atlas Digital Georreferenciado Amazonia IA

## Brief

Busca de informacao e brainstorm sobre o seguinte problema e produto que pode ser desenvolvido para o projeto:

**Problema**: Acesso controlado e curado a informacao multimodal referenciada geograficamente -- datazoom.amazonia, nova cartografia social da amazonia.

**Produto**: Atlas digital georreferenciado e iterativo assistido por IA (chat com ferramentas para navegacao na base de dados) para auxiliar na busca de informacao armazenada, mantida e curada por uma comunidade.

---

## Q&A Log

### Q1 -- 2026-04-24 01:08 UTC

**Pergunta**: O que e viavel tecnicamente, quais sao os desafios centrais e quais extensoes ao kb-qa permitiriam construir um MVP de atlas digital georreferenciado da Amazonia assistido por IA?

**Resposta**:

O kb-qa atual cobre 20-30% do que o atlas precisa. A stack atual (ChromaDB + sentence-transformers + MCP) funciona bem para recuperacao semantica textual, mas o atlas exige tres camadas ausentes:

1. Recuperacao geoespacial real (busca por bbox, poligono, raio -- nao possivel em ChromaDB).
2. Dados multimodais estruturalmente distintos (rasters, imagens, videos, relatos orais).
3. Controle de acesso por nivel de sensibilidade (dados de comunidades tradicionais).

**Perspectivas avaliadas**:

- ARCH [HIGH]: Arquitetura em camadas com DuckDB spatial (MVP) ou PostGIS (producao) como segunda engine de recuperacao geoespacial, orquestrada por agente com tools `query_knowledge` + `query_spatial` + `render_map`.
- SEC [HIGH]: Adicionar `sensitivity_level` nos metadados ChromaDB (`public`, `community_restricted`, `private`) com filtro nativo antes de ingerir qualquer dado do PNCSA ou FUNAI. Pre-requisito etico, nao feature.
- DATA [HIGH]: Principios CARE + OCAP como restricoes de design (co-governanca comunitaria, direito de remocao, proveniencia obrigatoria por chunk).
- PERF [HIGH]: Substituir `all-MiniLM-L6-v2` por `paraphrase-multilingual-mpnet-base-v2` para suporte a pt-BR; SatCLIP/GeoCLIP para imagens de satelite em versao futura.
- UX [MEDIUM]: Tool MCP `render_map` retornando PNG base64 ou link kepler.gl -- um atlas sem visualizacao nao e um atlas.
- OPS [MEDIUM]: Stack local aceitavel para MVP single-user; adicionar `reference_year` como metadado para coexistencia temporal de dados PRODES.

**Roadmap de extensoes (ordem de implementacao)**:

| # | Extensao | Prioridade |
|---|---|---|
| 1 | `sensitivity_level` no MCP + filtro ChromaDB | HIGH |
| 2 | Metadados CARE/OCAP em toda ingestao | HIGH |
| 3 | DuckDB spatial como segunda engine | HIGH |
| 4 | Tool MCP `query_spatial` | HIGH |
| 5 | Tool MCP `render_map` | MEDIUM |
| 6 | Pipeline de ingestao GeoJSON (TerraBrasilis/INPE) | MEDIUM |
| 7 | Substituir embedding model por multilingual | MEDIUM |
| 8 | Migrar para PostGIS (producao multi-usuario) | LOW |

**Fontes consultadas pelo agente de revisao**:
- GeoAgentic-RAG (ScienceDirect 2026): framework multi-agente para raciocinio geoespacial autonomo (85.3% pass rate)
- GeoGraphRAG (ScienceDirect 2025): abordagem graph-based para modelagem geoespacial
- RS-RAG (arXiv 2504.04988): RAG para imagens de sensoriamento remoto com encoders separados por modalidade
- CARE Principles for Indigenous Data Governance (Data Science Journal 2020)
- First Nations OCAP Principles (FNIGC)
- LLM-Geo (GitHub gladcolor): framework autonomo GIS com LLM
- datazoom.amazonia (GitHub datazoompuc): pacote R de acesso a dados abertos da Amazonia
- Elastic + Amazon Bedrock: geospatial RAG hibrido com kNN + geo-distance queries
