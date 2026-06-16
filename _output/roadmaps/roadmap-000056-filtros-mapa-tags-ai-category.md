# Roadmap 000056 | 2026-06-16 13:27 UTC | filtros-mapa-tags-ai-category

## Source
- fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py (read)
- fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/database/models.py (read)
- fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/security_reports.py (read)
- fala-gavea-seguranca/static/app.js (read)
- product-design/project/product-design-as-coded.md (read)
- product-design/project/product-design-as-intended.md (read)

## Context

O mapa de relatos de segurança já tem filtragem por `category`, `status`, `since`, e bbox (`lat_min/lat_max/lon_min/lon_max`) no backend, além de busca semântica via ChromaDB em `GET /security_reports/search`. O frontend (`app.js`) expõe apenas `category` e `status`. O objetivo deste roadmap é:

1. **Gerar um dataset fake** com dados realistas de Gávea para desenvolvimento.
2. **Tags livres** nos relatos — tags atribuídas pelo cidadão ou por IA, filtraveis no mapa.
3. **AI auto-categorização + curadoria pelo delegado** — a IA sugere a `ReportCategory` a partir do conjunto pré-estabelecido; o delegado (agente público) confirma ou corrige.
4. **Completar a filtragem no frontend** — expor filtro temporal (`date_from`/`date_to`), filtro espacial (extensão atual do mapa), tag chips, e barra de busca semântica.

### O que já existe (não precisa ser construído)
- `GET /security_reports/geojson?since=...&lat_min=...` etc. — filtragem backend ✅
- `GET /security_reports/search?q=...` — busca semântica ✅
- ChromaDB indexing on report creation ✅
- `ai_labels: list[str]` no domain entity + DB ✅ (vamos reutilizar para tags curadas por IA)

### Decisão de design — ReportCategory curada
Manter `ReportCategory` como Enum (o conjunto pré-estabelecido de interesse). A IA lê o texto do relato e escolhe o valor mais apropriado do Enum. O delegado confirma via `PATCH /{id}/category`. Novo campo `ai_suggested_category: ReportCategory | None` persiste a sugestão antes da confirmação.

Não moveremos as categorias para uma tabela DB nesta versão — o Enum é o catálogo curado, e mudanças no catálogo requerem um novo ciclo de design.

---

## Wave Summary

### Wave 0 — Fake Dataset (sequential, nenhuma dependência)
| # | ID | Title | Scope | Type | Plan | Status |
|---|-----|-------|-------|------|------|--------|
| 1 | fake-dataset | Script de seed: 250 relatos fake de Gávea | backend | technical | plan-TBD | pending |

**Escopo do item 1:**
- Script Python `fala-gavea-seguranca/scripts/seed_reports.py`
- 250 `SecurityReport` com coordenadas realistas dentro da Gávea (bbox: lat -22.965 a -22.990, lon -43.215 a -43.245)
- Datas distribuídas nos últimos 6 meses (2025-12-16 a 2026-06-16), com concentração maior nos últimos 30 dias
- Categorias distribuídas: 35% iluminacao, 30% transito, 20% vandalismo, 15% outro
- Textos em pt-BR plausíveis (10–30 variações por categoria, sorteio aleatório com leve variação)
- `territory_name` de 4 zonas da Gávea (Baixo Gávea, Alto da Gávea, Comunidade da Gávea, Jardim Botânico)
- `status`: 60% pendente, 25% em_analise, 15% resolvido
- `ai_labels: []` inicialmente (será preenchido pelo Wave 2)
- Idempotente via `DELETE FROM security_reports WHERE author_id LIKE 'seed-%'` antes do insert

---

### Wave 1 — Backend: Tags + AI-categorização (paralelo; dependem apenas da infra existente)
| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 2 | tags-model | Tags livres: campo + API | backend | technical | plan-TBD | — | pending |
| 3 | ai-category | AI auto-categorização + curadoria delegado | backend | technical | plan-TBD | — | pending |
| 4 | time-filter-until | Adicionar param `until` ao backend | backend | technical | plan-TBD | — | pending |

**Item 2 — Tags:**
- Novo campo `tags: list[str]` em `SecurityReport` (dataclass) e `SecurityReportModel` (JSON column, default `[]`)
- Alembic migration `add_tags_to_security_reports`
- `PATCH /security_reports/{id}/tags` — body `{"tags": ["string", ...]}`, substitui lista; usa novo use case `SetReportTags`
- Schema `SecurityReportTagsUpdate(tags: list[str])` em `security_report_schemas.py`
- `SecurityReportResponse` passa a incluir `tags: list[str]`
- Expor `tags` nas features do geojson endpoint
- Filtro `?tag=<valor>` no `GET /security_reports/geojson` — filtra por tag contida na lista (SQLite JSON_EACH ou LIKE `%"tag"%`)
- `ReportFilter` dataclass recebe campo `tag: str | None`

**Item 3 — AI auto-categorização + curadoria:**
- Novo campo `ai_suggested_category: ReportCategory | None` em `SecurityReport` + DB migration (`ai_suggested_category` nullable enum column)
- `POST /security_reports/{id}/auto_categorize` — chama Ollama com prompt pt-BR que lista as 4 categorias válidas e o texto do relato; retorna `{"category": "iluminacao"}` → salva em `ai_suggested_category`; não altera `category` (que é a categoria confirmada)
- `PATCH /security_reports/{id}/category` — body `{"category": "iluminacao"}`; uso pelo delegado para confirmar/corrigir; atualiza `category` e zera `ai_suggested_category`
- `OllamaClient` (reuso do padrão `gavealab_poc/llm.py`) via env `FALA_GAVEA_SEGURANCA_OLLAMA_URL` (default `http://localhost:11434/v1`) e `FALA_GAVEA_SEGURANCA_OLLAMA_MODEL` (default `qwen3:8b`)
- `SecurityReportResponse` passa a incluir `ai_suggested_category: str | None`
- Prompt template (pt-BR): lista os valores válidos do Enum + texto do relato → resposta JSON `{"category": "<valor>", "confidence": "<alta|media|baixa>", "justification": "<str>"}`

**Item 4 — Param `until`:**
- Adicionar `until: datetime | None` a `ReportFilter` e à query SQLAlchemy (`created_at <= until`)
- Expor `until: datetime | None = Query(None)` nos endpoints `GET /geojson` e `GET /`
- Testes unitários: filtro `since+until` produz apenas os relatos no intervalo

---

### Wave 2 — Frontend: painel de filtros completo (depende de Wave 1)
| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 5 | filter-ui | Painel de filtros: tempo, bbox, tags, busca | frontend | design+technical | plan-TBD | tags-model, ai-category, time-filter-until | pending |

**Item 5 — Frontend:**

*Filtro temporal:*
- Dois `<input type="date">` (`#filter-date-from`, `#filter-date-to`) no painel de filtros do `index.html`
- `buildQueryString()` inclui `since=<ISO>` e `until=<ISO>` quando preenchidos

*Filtro espacial (extensão do mapa):*
- Checkbox `#filter-bbox` "Somente área visível" — quando ativo, `buildQueryString()` lê `map.getBounds()` e adiciona `lat_min`, `lat_max`, `lon_min`, `lon_max`
- Update automático ao mover o mapa com o checkbox ativo (event `map.on('moveend', ...)`)

*Tags:*
- Input `#filter-tag` (texto livre) para filtrar por tag — passa `tag=<valor>` ao endpoint
- No popup de cada marker, exibir tags como chips `<span class="tag">` quando `p.tags.length > 0`
- Formulário de novo relato: campo `#f-tags` (input texto com instrução "separe por vírgulas") → enviado como array `tags`

*Busca semântica:*
- Campo `#search-q` + botão "Buscar" — chama `GET /security_reports/search?q=...&n=20` e exibe os resultados como pins roxos em layer separado (`searchLayerGroup`); ao clicar no pin, abre popup com texto e categoria
- Botão "Limpar busca" remove o layer e volta ao estado normal

*Painel "Curadoria de categoria" (delegado):*
- No popup de cada marker: se `p.ai_suggested_category` e `p.ai_suggested_category !== p.category`, exibir badge amarelo "🤖 Sugestão: <valor>" + dois botões "✅ Confirmar" (chama `PATCH /{id}/category` com o valor sugerido) e "✏️ Corrigir" (dropdown com 4 opções)
- Botão "🤖 Categorizar" no popup (acessível a delegado): chama `POST /{id}/auto_categorize` e reload do popup

---

## Execution Instructions

### Wave 0 (sequential — executar primeiro)
```
/implement plan-TBD  # fake-dataset (item 1)
```

### Wave 1 (parallel — executar em paralelo após Wave 0)
Os 3 itens são independentes entre si:
```
# Sessão 1:
/implement plan-TBD  # tags-model (item 2)

# Sessão 2:
/implement plan-TBD  # ai-category (item 3)

# Sessão 3:
/implement plan-TBD  # time-filter-until (item 4)
```
Ou em paralelo via worktree agents.

### Wave 2 (sequential — executar após Wave 1 completa)
```
/implement plan-TBD  # filter-ui (item 5)
```

> Os `plan-TBD` serão substituídos pelos IDs reais após `/plan` ser invocado para cada item.

---

## Notes para os planos individuais

- **Migrações Alembic**: o projeto usa SQLAlchemy + Alembic (padrão do roadmap-000054). Cada plano que adicionar colunas deve incluir uma migration `versions/` com `upgrade()` e `downgrade()`.
- **Testes**: manter cobertura existente; cada plano de backend deve incluir testes para os novos endpoints e o filtro adicionado.
- **Ollama**: o item 3 requer Ollama rodando localmente. Os testes do use case devem mockar a chamada HTTP.
- **Seed idempotência**: o script do item 1 deve ser re-executável sem duplicar dados.
