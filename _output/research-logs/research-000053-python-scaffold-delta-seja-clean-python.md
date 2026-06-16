# Research 000053 | research | 2026-06-16 00:35 UTC | python-scaffold delta para seja-clean-python
tags: architecture, scaffolding, geospatial, fastapi, leaflet

## User brief

Mapear o estado atual da skill python-scaffold e definir o delta para seja-clean-python: scaffold de CRUD REST clean architecture sobre qualquer entidade, com suporte a campos geoespaciais (lat/lon), upload de mídia, e frontend web interativo (Leaflet.js ou MapLibre GL) consumindo a REST API — Opção B confirmada (FastAPI REST + web component separado, mapa interativo de verdade). Objetivo: definir o que já existe, o que falta, e quais são as fundações para instanciar Fala Gávea - Segurança.

## Agent interpretation

Pesquisa de estado atual + análise de delta. O scaffold existente (`python-scaffold`) é lido integralmente. O delta é avaliado contra os dois casos de uso confirmados: (1) cidadão reporta problema de segurança com foto + localização, (2) delegado visualiza dashboard georreferenciado com filtros e chat. A decisão de arquitetura (Opção B: FastAPI + Leaflet.js web component) já foi tomada pelo usuário — esta pesquisa não questiona essa decisão, apenas define o que precisa ser adicionado ao scaffold para suportá-la.

## Files read

- `.claude/skills/python-scaffold/SKILL.md`
- `.claude/skills/python-scaffold/SKILL-quickguide.md`
- `.claude/skills/python-scaffold/scripts/scaffold.py` (1023 linhas — lido integralmente)

---

## Q&A log

### Q1: O que o `python-scaffold` atual já entrega?

O scaffold gera ~35 arquivos com clean architecture em 4 camadas via templates Python stdlib (sem Jinja2):

**Entidade gerada (hardcoded nos templates):**
- `id: str` (UUID)
- `text: str`
- `territory_level: TerritoryLevel` (enum: neighborhood/district/city)
- `territory_name: str`
- `author_id: str`
- `created_at: datetime`
- `ai_labels: list[str]` (extensão AI)
- `label_feedback: dict[str, bool]` (extensão AI)
- `likes_count: int` (sinal social)

**Endpoints CRUD gerados:**
- `POST /{entity_plural}/` → 201
- `GET /{entity_plural}/` → 200 (paginado: `limit`, `offset`)
- `GET /{entity_plural}/{id}` → 200 / 404
- `DELETE /{entity_plural}/{id}` → 204 / 404

**Tests gerados:**
- 10 unit tests (FakeRepository)
- 7 integration tests (TestClient, SQLite in-memory)

**O que NÃO está nos templates:**
- Nenhum campo geoespacial (lat, lon)
- Nenhum endpoint GeoJSON
- Nenhum CORS middleware
- Nenhum frontend / static files
- Nenhum campo `category` nem `status`
- Nenhum endpoint PATCH/update
- Nenhum filtro no endpoint de listagem
- Nenhum upload de arquivo/foto
- Nenhum ChromaDB

### Q2: Qual é o delta mínimo para Fala Gávea - Segurança funcionar com mapa interativo?

Delta mínimo (MVP em ordem de dependência):

1. `lat: float | None`, `lon: float | None` na entidade → model → schema → create input
2. `GET /relatos/geojson` → `FeatureCollection` com `geometry: Point` por relato com coordenadas
3. `CORSMiddleware` no `main.py` (origins via `.env`)
4. `static/index.html` com Leaflet.js + OpenStreetMap tiles servido em `GET /`
5. Campos `category` (enum parametrizável) e `status` (pendente/em_analise/resolvido)
6. `PATCH /{id}` + `UpdateSecurityReport` use case (muda status)
7. Filtros no `GET /`: `?category=`, `?status=`, `?since=`, `?bbox=`

Upload de foto é desejável mas não bloqueia o MVP.

### Q3: Como o `seja-clean-python` difere do `python-scaffold` conceitualmente?

`python-scaffold` é um gerador de projeto com entidade padrão (CitizenPost). `seja-clean-python` é um framework de instâncias: o scaffold aceita configuração de campos e features via CLI, e gera código adaptado. A diferença é:

```
python-scaffold fala-gavea-seguranca --entity SecurityReport
# → gera entidade com campos de CitizenPost, renomeados

seja-clean-python fala-gavea-seguranca \
  --entity SecurityReport \
  --categories iluminacao,transito,vandalismo \
  --features geospatial,cors,leaflet,file_upload
# → gera entidade com lat/lon/category/status/photo_url,
#    GeoJSON endpoint, CORS, static frontend com mapa
```

Internamente, o `scaffold.py` ganha blocos condicionais que são incluídos ou excluídos dependendo das features solicitadas.

---

## Recommendations summary

### R1 (HIGH) — Estender entity template com lat/lon + GeoJSON endpoint

**Campos:** `lat: float | None`, `lon: float | None` na entidade, model SQLAlchemy, e schemas Pydantic.

**Endpoint novo:** `GET /{entity_plural}/geojson` retorna `FeatureCollection`:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [lon, lat]},
      "properties": {"id": "...", "text": "...", "category": "...", "status": "..."}
    }
  ]
}
```

**Por que HIGH:** sem lat/lon não existe mapa. Sem GeoJSON endpoint o Leaflet não tem dados para plotar.

### R2 (HIGH) — CORS + frontend estático servido pelo FastAPI

**No `main.py`:**
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root() -> FileResponse:
    return FileResponse("static/index.html")
```

**Static folder gerado pelo scaffold:**
```
static/
├── index.html   ← Leaflet.js CDN + mapa fullscreen
├── app.js       ← fetch /geojson, renderiza pins, form de criação
└── style.css
```

**Por que HIGH:** Opção B exige web component separado. Sem isso, o cidadão e o delegado não têm interface.

### R3 (HIGH) — Campos `category` e `status` + endpoint PATCH

**Entidade estendida:**
```python
class ReportCategory(str, Enum):
    ILUMINACAO = "iluminacao"
    TRANSITO = "transito"
    VANDALISMO = "vandalismo"
    OUTRO = "outro"

class ReportStatus(str, Enum):
    PENDENTE = "pendente"
    EM_ANALISE = "em_analise"
    RESOLVIDO = "resolvido"
```

**`PATCH /{id}`** com schema `SecurityReportUpdate(status: ReportStatus)` → use case `UpdateSecurityReport`.

**Por que HIGH:** o delegado (caso de uso 2) precisa mudar o status dos relatos. Sem isso o dashboard é só leitura.

### R4 (MEDIUM) — Filtros no endpoint de listagem

`GET /relatos/?category=iluminacao&status=pendente&since=2026-06-01&bbox=-43.2,-22.9,-43.1,-22.8`

Implementado no `find_all()` do repository com WHERE clauses condicionais. O `bbox` filtra por `lat BETWEEN` e `lon BETWEEN`.

**Por que MEDIUM:** o mapa pode funcionar sem filtros (mostra tudo), mas o caso de uso do delegado fica muito limitado.

### R5 (MEDIUM) — Renomear skill para `seja-clean-python` com `--features` flag

```bash
/seja-clean-python fala-gavea-seguranca \
  --entity SecurityReport \
  --categories iluminacao,transito,vandalismo \
  --features geospatial,cors,leaflet
```

Features implementadas como blocos condicionais no `scaffold.py`. Ordem de implementação: `geospatial` → `cors` → `leaflet` → `file_upload` → `chromadb`.

**Por que MEDIUM:** para a primeira instância (Fala Gávea - Segurança) podemos gerar o código manualmente ou via `/plan`. O `seja-clean-python` genérico vem na segunda instância.

### R6 (LOW) — Upload de foto (multipart)

`POST /relatos/{id}/photo` aceita `multipart/form-data`, salva em `uploads/`, atualiza `photo_url` na entidade.

**Por que LOW:** os dois casos de uso funcionam sem foto para o MVP. A foto é um enhancement.

### R4-REVISED (HIGH) — Filtros geoespaciais e semânticos no endpoint de listagem

`GET /relatos/?category=iluminacao&status=pendente&since=2026-06-01&bbox=-43.2,-22.9,-43.1,-22.8`

O `bbox` filtra por `lat BETWEEN` e `lon BETWEEN` no SQLite. Os demais filtros são WHERE clauses condicionais no `find_all()` do repository.

Adicionalmente: `GET /relatos/search?q=poste+apagado&bbox=...` — query semântica no ChromaDB filtrada por metadado de localização, retorna IDs que são cruzados com o SQLite para dados completos.

**Por que HIGH (revisado):** o delegado não tem caso de uso sem filtros. O RAG georreferenciado é o diferencial da plataforma — não é enhancement.

### R7-REVISED (HIGH) — ChromaDB com metadados geoespaciais (RAG georreferenciado)

**Arquitetura dual-store:**

```
Relato criado pelo cidadão
    ↓
SQLite (fonte de verdade):           ChromaDB (índice semântico):
  id, text, lat, lon,                  id=relato_id,
  category, status, photo_url          embedding=embed(text),
  created_at, author_id                metadata={lat, lon, category, status}
```

**Use case `SearchSimilarReports`:**
```python
def execute(self, query: str, bbox: BBox | None, category: str | None) -> list[str]:
    where = {}
    if bbox:
        where["lat"] = {"$gte": bbox.lat_min, "$lte": bbox.lat_max}
    results = self._chroma.query(query_texts=[query], where=where)
    return results["ids"][0]  # cruza com SQLite
```

**Endpoint:** `GET /relatos/search?q=poste+apagado&bbox=-43.2,-22.9,-43.1,-22.8`

**Por que HIGH (revisado):** o delegado precisa de "relatos parecidos com este, na minha área" — isso só é possível com RAG + filtro geoespacial. É o diferencial da plataforma em relação a um CRUD convencional.

**Dependência:** ChromaDB suporta filtros de metadados nativamente via `where` clause. Lat/lon como metadados float funcionam com `$gte/$lte`. Não é necessário um índice espacial dedicado para o MVP.

### R8 (HIGH) — Chat RAG persistido com retroalimentação do índice

**Nova entidade: `ChatSession` + `ChatMessage`**

```
ChatSession
  id: str (UUID)
  delegate_id: str
  title: str             ← gerado pelo LLM a partir da primeira query
  created_at: datetime

ChatMessage
  id: str
  session_id: str
  role: "user" | "assistant"
  content: str
  sources: list[str]     ← IDs dos relatos/chats usados como contexto
  created_at: datetime
```

**Endpoints novos:**
- `POST /chats/` — cria sessão
- `POST /chats/{id}/messages` — envia query, retorna resposta RAG + LLM
- `GET /chats/` — lista sessões do delegado
- `GET /chats/{id}` — sessão completa com mensagens
- `GET /chats/insights` — clusters de intenção (UMAP sobre embeddings das queries)

**Pipeline RAG do chat (por mensagem):**
1. Delegate envia: *"Quais relatos de iluminação na área do Leblon este mês?"*
2. Sistema embede a query → ChromaDB search com where `{lat: ..., lon: ..., type: "$in", value: ["relato", "chat"]}`
3. Top-k resultados (relatos + respostas de chats anteriores) → contexto para o LLM
4. LLM (Ollama local) gera resposta estruturada com citações de fontes
5. Par query+resposta salvo no SQLite (`ChatMessage` com `sources`)
6. Par query+resposta indexado no ChromaDB com metadados `{type: "chat", delegate_id, session_id, lat_centroid, lon_centroid}`

**Retroalimentação — o sistema se alimenta de si mesmo:**

```
Relatos dos cidadãos           ChromaDB collection "fala-gavea-seguranca"
     ↓ ingest               ┌─ type: "relato" | metadados: lat, lon, category, status
ChatSession criada           └─ type: "chat"   | metadados: delegate_id, session_id, lat_centroid
     ↓ ingest
Próxima query encontra ambos: relatos E investigações anteriores como contexto
```

**Visualização de intenções:**
- Embeddings das queries do delegado → UMAP 2D (mesmo pipeline do gavealab-poc)
- Clusters revelam padrões: "delegado X investiga principalmente iluminação no Leblon às quintas"
- Essa visualização é o `GET /chats/insights` — um scatter plot de intenções, análogo ao cluster map do GaveaLab

**Por que HIGH:** o chat não é um feature isolado — é o mecanismo pelo qual o conhecimento operacional do delegado (o que ele investiga, com que frequência, em que área) vira dado estruturado. Sem persistência e reindexação, o sistema perde a memória institucional.
