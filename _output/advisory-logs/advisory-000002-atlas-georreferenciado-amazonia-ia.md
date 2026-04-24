# Advisory 000002 | FEATURE-X | 2026-04-24 01:12 UTC | Atlas Digital Georreferenciado Amazonia IA

tags: atlas-georreferenciado, amazonia, rag-geoespacial, soberania-de-dados, arquitetura, multimodal

---

## User Brief

Busca de informacao e brainstorm sobre o seguinte problema e produto que pode ser desenvolvido para o projeto:

**Problema**: Acesso controlado e curado a informacao multimodal referenciada geograficamente -- datazoom.amazonia, nova cartografia social da amazonia.

**Produto**: Atlas digital georreferenciado e iterativo assistido por IA (chat com ferramentas para navegacao na base de dados) para auxiliar na busca de informacao armazenada, mantida e curada por uma comunidade.

## Agent Interpretation

O usuario explora a viabilidade de estender o projeto kb-qa atual (RAG local com ChromaDB + sentence-transformers + MCP) para suportar um atlas digital da Amazonia com:

- Dados geoespaciais multimodais (vetores GeoJSON, rasters de satelite, documentos textuais, relatos orais, imagens)
- Fontes identificadas: datazoom.amazonia (pacote R com PRODES, DETER, SIMLAM, IMAZON, IBAMA, FUNAI) e Nova Cartografia Social da Amazonia/PNCSA (mapeamento participativo de povos e comunidades tradicionais)
- Interface conversacional com ferramentas para navegacao geoespacial
- Curadoria e governanca comunitaria da base de dados

## Files

- [_references/project/product-design-as-coded.md](_references/project/product-design-as-coded.md)
- [_references/project/constitution.md](_references/project/constitution.md)
- [agents/mcp_server.py](agents/mcp_server.py)
- [src/kb_qa/](src/kb_qa/)

---

## Q&A Log

### Q1

**Pergunta**: O que e viavel tecnicamente, quais sao os desafios centrais e quais extensoes ao kb-qa permitiriam construir um MVP de atlas digital georreferenciado da Amazonia assistido por IA?

**Resposta**:

#### Diagnostico: o kb-qa atual cobre 20-30% do que o atlas precisa

O pipeline atual (CLI Ingest -> Embed -> ChromaDB -> MCP query_knowledge) funciona bem para recuperacao semantica sobre texto (.md, .pdf). O atlas, porem, exige tres camadas que hoje estao ausentes:

1. **Recuperacao geoespacial real**: busca por bounding box, poligono de intersecao, raio de distancia. ChromaDB nao tem indices espaciais -- GeoJSON serializado como string perde toda a semantica geometrica.
2. **Dados multimodais estruturalmente distintos**: rasters (PRODES, MapBiomas, imagens de satelite), fotos, videos, relatos orais -- categorias sem pipeline de ingestao atual.
3. **Controle de acesso por nivel de sensibilidade**: dados de comunidades indigenas e tradicionais sao heterogeneos em sensibilidade; o MCP server atual expoe tudo sem autenticacao.

---

#### Perspectiva ARCH -- Arquitetura em camadas e o unico caminho viavel [HIGH]

A pesquisa atual (GeoAgentic-RAG, ScienceDirect 2026; LLM-Geo, GitHub gladcolor; GeoGraphRAG, ScienceDirect 2025) converge para uma arquitetura de duas engines de recuperacao orquestradas por um agente:

```
Agente LLM (Claude via MCP)
├── Tool: query_knowledge(query)   -> ChromaDB RAG (textos, relatos, PDFs)
├── Tool: query_spatial(bbox, sql) -> PostGIS / DuckDB spatial
└── Tool: render_map(geojson)      -> PNG base64 ou link kepler.gl
```

**Para MVP academico**: DuckDB + extensao `spatial` (lancada 2023, estavel 2024) substitui PostGIS sem servidor separado. Suporta ST_Intersects, ST_Area, ST_Distance, leitura nativa de GeoJSON e shapefiles.

**Para producao**: migrar para PostGIS (PostgreSQL + extensao PostGIS) quando escala ou concorrencia de usuarios exigir.

Pros: DuckDB e zero-config, arquivo local, API Python nativa, sem overhead de rede.
Contras: nao escala para multiplos usuarios concorrentes -- aceitavel para MVP academico.

---

#### Perspectiva SEC -- Controle de acesso e pre-requisito etico, nao feature futura [HIGH]

O MCP server atual aceita `query_knowledge` sem autenticacao. Para qualquer dado comunitario sensivel:

- Adicionar campo `sensitivity_level` nos metadados ChromaDB: `public`, `community_restricted`, `private`.
- Passar `access_level` como parametro do MCP e filtrar com `where={"sensitivity_level": {"$in": allowed_levels}}` -- ChromaDB suporta filtros de metadados nativamente.
- Dados do PNCSA com localizacao de comunidades entram como `community_restricted` por default.

Para MVP: token estatico simples (varavel de ambiente) como `access_level`. Para producao: JWT com roles.

Rationale critico: dados de localizacao de comunidades indigenas tem historico documentado de uso por atores mal-intencionados. Nao ha negociacao aqui -- e prerequisito etico e de seguranca antes de ingerir qualquer dado do PNCSA ou FUNAI.

---

#### Perspectiva DATA -- Soberania de dados: principios CARE + OCAP como restricoes de design [HIGH]

Os principios CARE (Collective Benefit, Authority to Control, Responsibility, Ethics) e OCAP (Ownership, Control, Access, Possession) -- adotados internacionalmente para governanca de dados indigenas -- impoe que:

- As comunidades sejam co-governantes dos dados, nao apenas sujeitos.
- Seja possivel revogar o consentimento e remover dados da base vetorial (`collection.delete(ids=[...])`).
- Cada chunk ingerido tenha metadados de proveniencia: `source`, `contributor`, `consent_scope`, `ingested_at`, `community_owner`.
- Um comite de governanca com representantes das comunidades revise o que entra na base.

Trade-off central: cumprir CARE significa que alguns dados nunca podem ser indexados ou devem ser deletaveis sob demanda, criando lacunas no corpus que afetam a qualidade das respostas RAG. A governanca comunitaria tem precedencia sobre a completude do indice -- sem excecao.

---

#### Perspectiva PERF -- Embeddings textuais sao inadequados para recuperacao geoespacial de precisao [HIGH]

sentence-transformers genericos (all-MiniLM-L6-v2) produzem embeddings semanticos de texto. Para dados geoespaciais:

- GeoJSON serializado como texto: dois poligonos adjacentes podem ter embeddings distantes por diferenca numerica de coordenadas.
- Rasters (GeoTIFF, NetCDF): sem representacao textual util para embeddings.

Arquitetura recomendada (baseada em RS-RAG, arXiv 2504.04988):

| Tipo de dado | Encoder recomendado |
|---|---|
| Texto cientifico, relatos | paraphrase-multilingual-mpnet-base-v2 (suporte pt-BR) |
| Imagens de satelite | SatCLIP ou GeoCLIP (pre-treinados em imagens georreferenciadas) |
| Metadados geometricos | Features numericas (centroide, bbox) para filtro pos-retrieval |

Para MVP: aceitar que imagens sejam recuperadas apenas por metadados textuais (descricao, data, regiao), reservando embeddings visuais para versao futura. Reduz dependencias pesadas (CLIP ~400MB).

---

#### Perspectiva UX -- Um atlas sem visualizacao cartografica nao e um atlas [MEDIUM]

Interface de chat textual nao expressa conceitos cartograficos. Pesquisas de UX em GIS mostram que usuarios esperam interacao espacial (zoom, pan, clique em regiao).

Solucao de baixa complexidade para o MVP:

- Implementar tool MCP `render_map(geojson, style)` usando `folium` ou `matplotlib + contextily` para retornar PNG base64.
- Claude pode exibir imagens base64 -- nao requer frontend separado.
- Alternativa mais simples: retornar link para geojson.io ou kepler.gl com dados codificados na URL.

Rationale: "encontrei 3 poligonos de desmatamento" sem mapa e uma resposta que nao permite ao usuario perceber o resultado -- breakdown de UX classico (Jakob Nielsen, sinalizar estado do sistema).

---

#### Perspectiva OPS -- Stack local incompativel com uso comunitario [MEDIUM]

O kb-qa e projetado para uso local individual. Um atlas comunitario requer:

- Acesso multi-usuario simultaneo.
- Atualizacao continua da base (novos relatos, novos dados INPE).
- Versionamento de dados geoespaciais (PRODES 2020 nao sobrescreve PRODES 2023).
- Backup da base vetorial (atualmente gitignored e efemera).

Para MVP academico: aceitar as limitacoes operacionais, documentar explicitamente que o sistema e single-user. Adicionar `reference_year` como metadado em todos os chunks para permitir filtros temporais sem sobrescrita.

---

#### Pipeline de ingestao do datazoom.amazonia [MEDIUM]

O datazoom.amazonia e um pacote R que acessa PRODES, DETER, IMAZON, SIMLAM, IBAMA, FUNAI. Duas opcoes:

- **Opcao A (simples)**: script R exporta para GeoJSON/CSV -> ingestor Python converte para metadados textuais + geometria DuckDB.
- **Opcao B (recomendada)**: acesso direto as APIs REST publicas do INPE via TerraBrasilis, sem dependencia de pacote R em producao. PRODES e DETER tem endpoints REST documentados.

Estender `src/kb_qa/ingestion/` para suportar GeoJSON como novo tipo de fonte, alem de .md e .pdf.

---

#### Resumo executivo: o que construir, em que ordem

| # | Extensao | Prioridade | Complexidade | Prerequisito |
|---|---|---|---|---|
| 1 | Modelo de controle de acesso por sensitivity_level no MCP | HIGH | Baixa | Nenhum -- implementar ANTES de ingerir qualquer dado sensivel |
| 2 | Metadados de proveniencia em toda ingestao (CARE/OCAP) | HIGH | Baixa | #1 |
| 3 | DuckDB spatial como engine de queries geoespaciais | HIGH | Media | #1 |
| 4 | Tool MCP `query_spatial` orquestrando RAG + espacial | HIGH | Media | #3 |
| 5 | Tool MCP `render_map` (PNG base64 ou link kepler.gl) | MEDIUM | Baixa | #3 |
| 6 | Pipeline de ingestao de GeoJSON (datazoom / TerraBrasilis) | MEDIUM | Media | #3 |
| 7 | Embeddings multimodais para imagens de satelite (SatCLIP) | MEDIUM | Alta | #6 |
| 8 | Migrar para PostGIS em caso de uso multi-usuario | LOW | Alta | #3 |

---

## Recommendations Summary

| # | Recomendacao | Prioridade |
|---|---|---|
| R1 | Implementar controle de acesso por `sensitivity_level` no MCP server ANTES de ingerir qualquer dado comunitario | HIGH |
| R2 | Adotar CARE + OCAP como restricoes de design: proveniencia, consentimento, direito de remocao por chunk | HIGH |
| R3 | Adicionar DuckDB spatial como segunda engine de recuperacao para queries geoespaciais reais | HIGH |
| R4 | Expor `query_spatial` como tool MCP adicional, orquestrado pelo mesmo agente que `query_knowledge` | HIGH |
| R5 | Implementar `render_map` tool MCP para saida visual cartografica (PNG base64 ou link kepler.gl) | MEDIUM |
| R6 | Construir pipeline de ingestao GeoJSON a partir de APIs do TerraBrasilis/INPE (sem dependencia de R) | MEDIUM |
| R7 | Usar `paraphrase-multilingual-mpnet-base-v2` para embeddings em portugues (en lugar de all-MiniLM) | MEDIUM |
| R8 | Para MVP: aceitar limitacoes de escala (single-user, DuckDB local), documentar explicitamente, migrar depois | LOW |
