# Roadmap 000054 | 2026-06-16 00:37 UTC | Fala Gávea - Segurança

source: research-000053 — python-scaffold delta para seja-clean-python com RAG georreferenciado e chat RAG

## Contexto

**Fala Gávea - Segurança** é a primeira instância da plataforma `seja-clean-python` — um framework de aplicações CRUD cidadãs georreferenciadas com RAG semântico. Cada instância cobre uma vertical temática (Segurança, Transporte, Saúde) com a mesma arquitetura base.

### Casos de uso confirmados

**UC-1 — Cidadão reporta problema de segurança:**
Um morador abre o mapa no browser, clica numa localização (ou permite GPS), preenche um formulário (texto, categoria) e envia. O relato vai para o SQLite + ChromaDB com metadados geoespaciais.

**UC-2 — Delegado / agente público explora o dashboard:**
Um agente público abre o mapa, visualiza os relatos como pins coloridos por categoria/status, filtra por área (bbox), categoria, status e data. Usa o chat RAG para fazer perguntas como "Quais relatos de iluminação no Leblon este mês?" e recebe respostas estruturadas com citações. Os chats são persistidos e reindexados — o sistema se retroalimenta.

### Decisão de arquitetura (Opção B confirmada)

```
fala-gavea-seguranca/
├── src/fala_gavea_seguranca/         ← FastAPI + SQLAlchemy + SQLite
│   ├── domain/                       ← SecurityReport, ChatSession, ChatMessage
│   ├── application/use_cases/        ← CRUD + GeoJSON + Search + Chat RAG
│   ├── infrastructure/
│   │   ├── database/                 ← SQLite (fonte de verdade)
│   │   ├── vector_store/             ← ChromaDB dual-store (relatos + chats)
│   │   └── llm/                      ← Ollama client (local, qwen3:8b)
│   └── presentation/api/             ← FastAPI + CORS + StaticFiles
└── static/                           ← HTML/JS puro (Leaflet.js + OpenStreetMap)
    ├── index.html                    ← Mapa interativo (UC-1 + UC-2 base)
    ├── chat.html                     ← Interface chat RAG (UC-2 avançado)
    └── insights.html                 ← UMAP de intenções do delegado
```

**Dual-store:** SQLite é fonte de verdade para dados estruturados. ChromaDB é índice derivado (pode ser reconstruído do SQLite) com metadados `{lat, lon, category, status, type: "relato"|"chat"}` para RAG georreferenciado.

---

## Source

- `_output/research-logs/research-000053-python-scaffold-delta-seja-clean-python.md` (read)
- `.claude/skills/python-scaffold/scripts/scaffold.py` (read — base do scaffold)
- `product-design/project/product-design-as-intended.md` (read)
- `product-design/project/conventions.md` (read)

---

## Modelo de Dados

```
SecurityReport {
  id           TEXT PRIMARY KEY        -- UUID
  text         TEXT NOT NULL           -- descrição do problema
  category     TEXT NOT NULL           -- 'iluminacao'|'transito'|'vandalismo'|'outro'
  status       TEXT NOT NULL DEFAULT 'pendente'  -- 'pendente'|'em_analise'|'resolvido'
  lat          REAL                    -- coordenada GPS (nullable se usuário não permitiu)
  lon          REAL
  territory_name TEXT                  -- nome do bairro/logradouro (texto livre)
  author_id    TEXT NOT NULL           -- UUID anônimo do cidadão
  photo_url    TEXT                    -- caminho local da foto (nullable)
  created_at   TEXT NOT NULL           -- ISO-8601 UTC
}

ChatSession {
  id           TEXT PRIMARY KEY        -- UUID
  delegate_id  TEXT NOT NULL           -- UUID ou identificador do agente público
  title        TEXT                    -- gerado pelo LLM da primeira query
  created_at   TEXT NOT NULL
}

ChatMessage {
  id           TEXT PRIMARY KEY        -- UUID
  session_id   TEXT NOT NULL REFERENCES chat_sessions(id)
  role         TEXT NOT NULL           -- 'user' | 'assistant'
  content      TEXT NOT NULL
  sources      TEXT                    -- JSON array de IDs (relatos ou chats usados como contexto)
  created_at   TEXT NOT NULL
}
```

---

## Wave Summary

### Wave 0 — Scaffold base (sequential)

| # | ID | Title | Scope | Type | Plan | Status |
|---|---|---|---|---|---|---|
| 1 | scaffold-base | Gerar fala-gavea-seguranca via python-scaffold estendido | backend | technical | plan-TBD | pending |

**Entrega:** projeto `fala-gavea-seguranca/` com entidade `SecurityReport` (campos: text, category, status, lat, lon, territory_name, author_id, photo_url), CORS middleware, StaticFiles config, pasta `static/` com placeholder `index.html`. Todos os testes passando.

### Wave 1 — Mapa interativo (sequential)

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|---|---|---|---|---|---|---|
| 2 | geojson-endpoint | GET /security_reports/geojson + endpoint PATCH status | backend | technical | plan-TBD | scaffold-base | pending |
| 3 | leaflet-frontend | Frontend Leaflet.js (index.html + app.js + style.css) | frontend | design | plan-TBD | geojson-endpoint | pending |

**Entrega:** mapa funcional no browser — cidadão vê pins dos relatos, clica para ver detalhes, abre formulário de criação. Delegado vê painel lateral básico.

### Wave 2 — Filtros + ChromaDB RAG (sequential)

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|---|---|---|---|---|---|---|
| 4 | filters | Filtros bbox/category/status/since no GET /security_reports/ | backend | technical | plan-TBD | geojson-endpoint | pending |
| 5 | chromadb-dualstore | ChromaDB dual-store: ingest relatos + GET /security_reports/search?q=&bbox= | backend | technical | plan-TBD | filters | pending |

**Entrega:** delegado filtra relatos no mapa por área, categoria e status. Busca semântica retorna relatos relevantes por query de texto + filtro geoespacial.

### Wave 3 — Chat RAG persistido (sequential)

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|---|---|---|---|---|---|---|
| 6 | chat-entities | ChatSession + ChatMessage: SQLite schema + CRUD endpoints | backend | technical | plan-TBD | chromadb-dualstore | pending |
| 7 | chat-rag-pipeline | Pipeline RAG: embed → ChromaDB → Ollama → save → reindex + chat.html | fullstack | technical | plan-TBD | chat-entities | pending |
| 8 | chat-insights | GET /chats/insights (UMAP de intenções) + insights.html | fullstack | technical | plan-TBD | chat-rag-pipeline | pending |

**Entrega:** delegado usa chat para fazer perguntas em linguagem natural sobre os relatos. Cada conversa é salva e reindexada no ChromaDB. A visualização de insights mostra clusters de intenção do delegado via UMAP.

---

## Execution Instructions

### Wave 0 (sequential — 1 plano)

```
/plan fala-gavea-seguranca Wave 0: gerar projeto via python-scaffold com entidade SecurityReport (text, category, status, lat, lon, territory_name, author_id, photo_url), CORS, StaticFiles
```

### Wave 1 (sequential — 2 planos)

Execute em ordem:
1. `/plan fala-gavea-seguranca Wave 1a: GET /security_reports/geojson (FeatureCollection) + PATCH /{id} (status update)`
2. `/plan fala-gavea-seguranca Wave 1b: frontend Leaflet.js — index.html + app.js + style.css servidos em GET /`

### Wave 2 (sequential — 2 planos)

Execute em ordem:
1. `/plan fala-gavea-seguranca Wave 2a: filtros bbox/category/status/since no GET /security_reports/`
2. `/plan fala-gavea-seguranca Wave 2b: ChromaDB dual-store — ingest relatos ao criar + GET /security_reports/search`

### Wave 3 (sequential — 3 planos)

Execute em ordem:
1. `/plan fala-gavea-seguranca Wave 3a: ChatSession + ChatMessage SQLite schema + CRUD REST`
2. `/plan fala-gavea-seguranca Wave 3b: pipeline RAG chat (ChromaDB → Ollama → save → reindex) + chat.html`
3. `/plan fala-gavea-seguranca Wave 3c: GET /chats/insights (UMAP embeddings das queries) + insights.html`

---

## Dependências externas

| Dependência | Onde usar | Observação |
|---|---|---|
| Ollama (`qwen3:8b`) | Wave 3b | Deve estar rodando em `localhost:11434`; mesmo padrão do gavealab-poc |
| sentence-transformers (`nomic-ai/nomic-embed-text-v1`) | Wave 2b | Download ~274MB no primeiro uso |
| ChromaDB (`>=0.5`) | Wave 2b | Embedded, sem servidor separado |
| Leaflet.js (CDN) | Wave 1b | Sem API key — usa OpenStreetMap tiles |

---

## Critérios de conclusão

- [ ] Wave 0: `uv run pytest -v` passa 100% no projeto gerado
- [ ] Wave 1: mapa abre no browser, pins aparecem, formulário de criação funciona
- [ ] Wave 2: filtro por bbox funciona no mapa; busca semântica retorna resultados relevantes
- [ ] Wave 3: delegado faz pergunta no chat e recebe resposta com fontes citadas; chat aparece em `/chats/`; insights.html mostra scatter plot de intenções
