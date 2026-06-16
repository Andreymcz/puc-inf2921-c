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

### Wave 0 — Fake Dataset ✅ DONE
| # | ID | Title | Scope | Type | Plan | Status |
|---|-----|-------|-------|------|------|--------|
| 1 | fake-dataset | Enriquecer ReportCategory (9 categorias) + seed script + prompt IA | backend | technical | plan-000057 | **done** |

**Escopo do item 1:**
- Script Python `fala-gavea-seguranca/scripts/seed_reports.py`
- 250 `SecurityReport` com coordenadas realistas dentro da Gávea (bbox: lat -22.965 a -22.990, lon -43.215 a -43.245)
- Datas distribuídas nos últimos 6 meses (2025-12-16 a 2026-06-16), com concentração maior nos últimos 30 dias
- Categorias distribuídas (derivadas do Forum de Seguranca LGD — plan-000057):
  28% furto_roubo, 22% iluminacao, 18% transito, 12% espaco_publico_inseguro,
  8% vandalismo, 5% moradores_situacao_rua, 4% conflito_social, 2% barulho_perturbacao, 1% outro
- Textos em pt-BR plausíveis (10–30 variações por categoria, sorteio aleatório com leve variação)
- `territory_name` de 4 zonas da Gávea (Baixo Gávea, Alto da Gávea, Comunidade da Gávea, Jardim Botânico)
- `status`: 60% pendente, 25% em_analise, 15% resolvido
- `ai_labels: []` inicialmente (será preenchido pelo Wave 2)
- Idempotente via `DELETE FROM security_reports WHERE author_id LIKE 'seed-%'` antes do insert

---

### Wave 1 — Backend: Tags + AI-categorização ✅ DONE
| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 2 | tags-model | Tags livres: campo + API | backend | technical | plan-000060 | fake-dataset | **done** |
| 3 | ai-category | AI auto-categorização + curadoria delegado | backend | technical | plan-000061 | fake-dataset | **done** |
| 4 | time-filter-until | Adicionar param `until` ao backend | backend | technical | plan-000062 | — | **done** |

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
- `POST /security_reports/{id}/auto_categorize` — chama Ollama com prompt pt-BR que lista as 9 categorias válidas (ver `CATEGORIZE_PROMPT` em `infrastructure/ai/prompts.py`, criado pelo plan-000057 Step 3) e o texto do relato; retorna `{"category": "furto_roubo", "confidence": "alta|media|baixa", "justification": "..."}` → salva em `ai_suggested_category`; não altera `category` (que é a categoria confirmada)
- `PATCH /security_reports/{id}/category` — body `{"category": "iluminacao"}`; uso pelo delegado para confirmar/corrigir; atualiza `category` e zera `ai_suggested_category`
- `OllamaClient` (reuso do padrão `gavealab_poc/llm.py`) via env `FALA_GAVEA_SEGURANCA_OLLAMA_URL` (default `http://localhost:11434/v1`) e `FALA_GAVEA_SEGURANCA_OLLAMA_MODEL` (default `qwen3:8b`)
- `SecurityReportResponse` passa a incluir `ai_suggested_category: str | None`
- Prompt template (pt-BR): já implementado em `infrastructure/ai/prompts.py::CATEGORIZE_PROMPT` pelo plan-000057 Step 3 — lista as 9 categorias com descrição + texto do relato → resposta JSON `{"category": "<valor>", "confidence": "<alta|media|baixa>", "justification": "<str>"}`

**Item 4 — Param `until`:**
- Adicionar `until: datetime | None` a `ReportFilter` e à query SQLAlchemy (`created_at <= until`)
- Expor `until: datetime | None = Query(None)` nos endpoints `GET /geojson` e `GET /`
- Testes unitários: filtro `since+until` produz apenas os relatos no intervalo

---

### Wave 2 — Frontend: painel de filtros completo 🔴 EM FOCO
| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 5 | filter-ui | Painel de filtros: tempo, bbox, tags, busca, curadoria IA | frontend | design+technical | plan-000063 | Wave 1 completa ✅ | **em andamento** |

> **Decisão de stack (research-000059, 2026-06-16):** Adoptar Alpine.js via CDN para gerenciar estados reativos da UI (especialmente o popup de curadoria multi-estado). Manter vanilla JS para inicialização do Leaflet e chamadas fetch. Sem bundler, sem npm build. Ativar Alpine dentro dos popups Leaflet com `Alpine.initTree(e.popup.getElement())` no evento `popupopen`.

**Item 5 — Frontend (plan-000063):**

*Step 1 — 9 categorias em CATEGORY_COLORS, CATEGORY_LABELS e selects:*
- Atualizar constantes em `app.js` + dropdowns em `index.html` para as 9 categorias do Wave 0

*Step 2 — Filtro temporal (date_from / date_to):*
- Dois `<input type="date">` (`#filter-date-from`, `#filter-date-to`) em `index.html`
- `buildQueryString()` inclui `since=<ISO>` e `until=<ISO>`

*Step 3 — Filtro espacial (bbox área visível):*
- Checkbox `#filter-bbox` "Somente área visível" em `index.html`
- `buildQueryString()` lê `map.getBounds()` e adiciona `lat_min/lat_max/lon_min/lon_max`
- `map.on('moveend', ...)` recarrega pins quando checkbox ativo + debounce 300ms

*Step 4 — Tags: filtro + chips no popup + campo no formulário:*
- Input `#filter-tag` na sidebar → passa `?tag=<valor>` ao endpoint
- Chips `<span class="tag-chip">` no popup de cada marker
- Campo `#f-tags` no formulário de novo relato ("separe por vírgulas") → enviado como `tags[]`

*Step 5 — Busca semântica:*
- Campo `#search-q` + botão "🔍 Buscar" → `GET /security_reports/search?q=...&n=20`
- Resultados como pins roxos em `searchLayerGroup` separado
- Botão "✕ Limpar busca" remove o layer

*Step 6 — Painel de curadoria de categoria (popup reativo):*
- Alpine.js CDN adicionado ao `index.html` (`<script defer src="cdn.alpinejs.dev/...">`)
- `map.on('popupopen', e => Alpine.initTree(e.popup.getElement()))` ativa Alpine nos popups
- Popup usa `x-data`, `x-show`, `x-on` para gerenciar os 3 estados:
  - **sem sugestão**: botão "🤖 Categorizar" (chama `POST /{id}/auto_categorize`)
  - **sugestão pendente**: badge amarelo + "✅ Confirmar" + dropdown "✏️ Corrigir"
  - **em loading/erro**: spinner `x-show="loading"` / badge vermelho `x-show="error"`

---

## Execution Instructions

### Wave 0 ✅ Concluída — plan-000057

### Wave 1 ✅ Concluída
- plan-000060: tags livres campo + API ✅
- plan-000061: auto-categorização + curadoria delegado ✅
- plan-000062: parâmetro until no backend ✅

### Wave 2 🔴 EM ANDAMENTO — próximo passo
```
/implement 63  # filter-ui: painel de filtros completo + Alpine.js + curadoria popup
```

> **Nota Alpine.js (research-000059):** O plan-000063 (Step 6) deve ser executado com Alpine.js para gerenciar o popup de curadoria. A adição de `Alpine.initTree()` no evento `popupopen` é o único ajuste em relação ao plan original. Os demais steps (1-5) são vanilla JS puro.

---

## Notes para os planos individuais

- **ReportCategory (9 categorias)**: o enum foi enriquecido pelo plan-000057 (derivado do Forum de Seguranca LGD). Os 9 valores são: `furto_roubo`, `iluminacao`, `transito`, `espaco_publico_inseguro`, `vandalismo`, `moradores_situacao_rua`, `conflito_social`, `barulho_perturbacao`, `outro`. O prompt de IA e o seed script estão detalhados em plan-000057 Steps 2-3.
- **Migrações**: o projeto usa `Base.metadata.create_all()` no startup (sem Alembic). Adicionar colunas requer deletar `app.db` e reiniciar (SQLite, ambiente de dev). Não há `versions/` a manter.
- **Testes**: manter cobertura existente; cada plano de backend deve incluir testes para os novos endpoints e o filtro adicionado.
- **Ollama**: o item 3 requer Ollama rodando localmente. Os testes do use case devem mockar a chamada HTTP.
- **Seed idempotência**: o script do item 1 deve ser re-executável sem duplicar dados.
