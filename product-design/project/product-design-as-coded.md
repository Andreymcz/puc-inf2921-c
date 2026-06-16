---
designer_description: "Implementation state mirror for kb-qa — maintained by post-skill after each plan execution."
---

# AS-CODED — INF2921-Grupo-C / kb-qa

<!-- maintained-by: Agent (post-skill); Agent classification since SEJA 2.8.4 -->

---

## Conceptual Design

### 0b. Fala Gávea — Streamlit frontend (plan-000030, plan-000032, plan-000033, plan-000036, plan-000043)

`fala-gavea/app.py` is the navigation entry point for the Fala Gávea Streamlit app. It calls `st.navigation()` + `st.Page()` (Streamlit 1.28+ API) and delegates each page to `fala-gavea/app_pages/<page>.py`. The API base URL defaults to `http://localhost:8000`, overridable via `FALA_GAVEA_API_URL`. A `user_id` UUID is generated once per session and stored in `st.session_state`. Shared helpers (`api_get`, `api_post`, `citizen_name`, `API_URL`, `POSTS_PER_PAGE`, `_CITIZEN_NAMES`) live in `fala-gavea/app_pages/shared.py`.

**Six pages** (dispatched via `st.navigation()`; each module exports `render() -> None`):
- **📋 Postagens**: paginated list of posts (20 per page, controlled by `st.session_state.posts_page`); prev/next controls fetch `POSTS_PER_PAGE=20` posts at the correct `offset`. Author displayed as a human-readable Brazilian first name via `citizen_name()` instead of a truncated UUID. When `likes_count > 0`, a `st.expander("Ver quem curtiu")` appears — likers are lazy-loaded: the expander shows a "Carregar curtidas" button; on click, fetches `GET /citizen_posts/{id}/likes` once and caches the result in `st.session_state[f"likers_{post_id}"]`. Subsequent renders read from cache — zero API calls on page load (plan-000040).
- **✍️ Nova Postagem**: form to create a new post (text + territory level/name); calls `POST /citizen_posts/`.
- **🏷️ Validar Labels**: shows posts that have `ai_labels`; per-label 👍/👎 buttons call `POST /citizen_posts/{id}/label_feedback`. Vote state reads from `label_feedback[label]["approved"]` (new dict structure).
- **📊 Dashboard**: summary metrics (total posts, total likes, avg likes per post), top-10 posts by likes, bar chart of posts by territory, "Postagens por dia" timeline (line chart on `created_at`), "Distribuição de likes por post" histogram (bucketed by `pd.cut` into 8 ranges ending at `float("inf")`), label feedback summary table, and two traceability subsections: "Rastreabilidade de likes" (on-demand bulk fetch; likers shown as names via `citizen_name()`) and "Rastreabilidade de labels" (reads `label_feedback` dict; user shown as name). Limit raised to 1500 to accommodate the seed dataset (plan-000032).
- **📥 Inserção em Massa (plan-000045)**: CSV file upload page for bulk post creation. Validates required columns (`text`, `territory_level`, `territory_name`, `author_id`); shows an error for missing columns; warns and filters rows with invalid `territory_level` values; previews up to 20 rows; on "Criar Postagens" click calls `POST /citizen_posts/bulk` and reports the count of created posts.
- **🗺️ Explorar Clusters (plan-000039, plan-000041, plan-000049, plan-000042)**: two-button layout — "Gerar Clusters" triggers the full pipeline; "Salvar Labels" persists results via API (disabled until clusters are generated). Results cached in `st.session_state.cluster_df`. A collapsed `⚙️ Parâmetros de clusterização` expander above the buttons exposes three sliders: `n_neighbors` (2–50, default 15), `min_dist` (0.01–0.5, default 0.1), `min_cluster_size` (2–20, default 5); values are passed to `build_cluster_df`. After generating, a noise-count `st.info` hint appears when any posts land in `cluster_id = -1`, suggesting which params to reduce (plan-000049). Shows an interactive Plotly scatter plot (UMAP-1/UMAP-2 axes, color by `cluster_label`, hover shows `text` and `territory_name`) and a "Posts por Cluster" section: non-noise clusters sorted by post count descending, noise last; each cluster is an `st.expander` titled `"{label}  ({n} posts)"` containing a `Relato` / `Territorio` dataframe and a per-cluster "🤖 Gerar label com IA" button (non-noise clusters only). Clicking that button calls `label_clusters` for that single cluster, updates `st.session_state.cluster_df` in-place, and triggers `st.rerun()`. On cluster generation, labels are set to default placeholders (`"Não classificado"` for noise, `"Cluster N"` for real clusters) — no LLM calls happen automatically (plan-000042).

**UMAP cluster pipeline (plan-000039)** — `fala-gavea/src/fala_gavea/pipeline/`:
- `embeddings.py`: `embed_and_store(posts, vectorstore_dir?)` encodes post texts with `nomic-ai/nomic-embed-text-v1` (prefix `search_document:`, `trust_remote_code=True`, cosine similarity) and upserts to ChromaDB `PersistentClient` at `fala-gavea/vectorstore/` (collection `fala-gavea-posts`). Idempotent (upsert by post ID). `get_embeddings(post_ids)` retrieves stored vectors. Both model and collection are `lru_cache(maxsize=1)` singletons. `sentence_transformers` is imported lazily inside `_get_model()` so the module can be imported in test contexts without loading the model (plan-000044).
- `cluster.py`: `build_cluster_df(posts, vectorstore_dir?, n_neighbors=15, min_dist=0.1, min_cluster_size=5)` retrieves pre-stored embeddings via `get_embeddings` (embeddings are persisted at post-creation time — no re-encoding here), projects to 2D via `umap.UMAP` (cosine, `random_state=42`, `n_neighbors` clamped to `min(n_neighbors, len(posts)-1)`), and clusters with `sklearn.cluster.HDBSCAN` (`min_cluster_size` clamped to `max(2, len(posts)//10)`). Returns a DataFrame with `post_id, text, territory_name, author_id, x, y, cluster_id, cluster_label`. Noise points have `cluster_id = -1`. (updated plan-000047)
- `label_clusters.py`: `label_clusters(df) -> dict[int, str]` calls Ollama (`FALA_GAVEA_OLLAMA_URL`, default `http://localhost:11434/v1`; `FALA_GAVEA_OLLAMA_MODEL`, default `qwen3:8b`) once per cluster with a pt-BR prompt and 5 representative posts (closest to centroid in UMAP space). Noise cluster (-1) maps to `"Não classificado"`. Logs `INFO` lines `LLM request: model=... cluster=...` and `LLM response: cluster=... label=...` per call. When `FALA_GAVEA_DEBUG_LLM=1`, additionally logs full prompt and raw response at INFO as `[DEBUG_LLM]` prefixed lines. On LLM failure logs `WARNING: LLM call failed for cluster N: <exc>` (no longer silently swallows exceptions) and falls back to `"Cluster N"` (plan-000042).

**Embed on creation + bulk post route (plan-000044)**:
- `CitizenPostRepository.save_many(entities)` — abstract method; `SQLAlchemyCitizenPostRepository` merges each entity and commits once.
- `BulkCreateCitizenPosts` use case in `application/use_cases/bulk_create_citizen_posts.py` — validates each `CreateCitizenPostInput` (fail-fast), creates domain entities, delegates to `repo.save_many`. Empty list is a no-op (returns `[]`).
- `BulkCitizenPostsCreate(items: list[CitizenPostCreate])` and `BulkCitizenPostsResponse(items: list[CitizenPostResponse])` schemas in `citizen_post_schemas.py`.
- `POST /citizen_posts/` — now calls `embed_and_store([...])` after saving, keeping the vector store current on every creation.
- `POST /citizen_posts/bulk` — registered before `/{id}` (path-matching order); accepts `BulkCitizenPostsCreate`, saves all posts in one `save_many` call, embeds all in one batched `embed_and_store` call, returns 201 with `BulkCitizenPostsResponse`.
- `conftest.py` autouse fixture `mock_embed` patches `embed_and_store` so no test loads the sentence-transformer model.

**`set_ai_labels` domain method (plan-000039)**:
- `CitizenPostRepository.set_ai_labels(post_id, labels)` — abstract method added.
- `SQLAlchemyCitizenPostRepository.set_ai_labels` — replaces `ai_labels` JSON column and commits; raises `CitizenPostNotFoundError` on missing post.
- `SetAiLabels` use case in `application/use_cases/set_ai_labels.py` — `execute(SetAiLabelsInput(post_id, labels))`.
- `POST /citizen_posts/{id}/ai_labels` — body `{"labels": ["label1"]}`, response `CitizenPostResponse`.
- `AiLabelsRequest(labels: list[str])` schema added to `citizen_post_schemas.py`.

**Citizen name helper (plan-000036)**: `citizen_name(user_id: str) -> str` maps any UUID to a deterministic Brazilian first name using MD5 hash modulo 30. `_CITIZEN_NAMES` is a 30-entry list of common Brazilian first names. Used everywhere UUIDs were previously displayed (`author_id`, `user_id` in likes, dashboard traceability columns).

**API helpers**: `api_get(path, **params)` and `api_post(path, body)` call the backend synchronously via `httpx` with a 10-second timeout and raise on 4xx/5xx.

**Seed script (plan-000032, fixed plan-000036)**: `fala-gavea/scripts/seed_db.py` reads `data/sample-gavealab-1000.csv` (UTF-8 encoding — fixed from latin-1 in plan-000036 to prevent Mojibake, columns: `id`, `comment`, `territory`). Maps 4 territory values to `territory_name`/`territory_level` pairs (Comunidade da Gávea, Baixo Gávea, Alto da Gávea, Favela da Gávea — all `neighborhood`). Each relato gets a unique `author_id` UUID. Posts inserted with `ai_labels: []`. After inserting all posts, each author distributes 50 likes to posts of other authors (excludes own post) via `POST /citizen_posts/{id}/likes` — ~50,000 sequential HTTP calls. Progress logged every 100 posts / 100 authors. Package marker `fala-gavea/scripts/__init__.py` also added.

**Like and label traceability (plan-000033)**:
- `GET /citizen_posts/{id}/likes` returns `PostLikesResponse{post_id, likers: [{user_id, created_at}]}` — implemented by `GetPostLikes` use case and `SQLAlchemyCitizenPostRepository.get_likes`.
- `label_feedback` JSON column stores `{label: {"approved": bool, "user_id": str}}` — `set_label_feedback` persists `user_id` alongside the flag.
- `LikeRecord` domain dataclass: `user_id: str, created_at: datetime`. `CitizenPostRepository` exposes `get_likes(post_id) -> list[LikeRecord]`.

### 0e. Fala Gávea Segurança — AI auto-categorização + curadoria pelo delegado (plan-000061)

**`SecurityReport` entity** — `domain/entities/security_report.py`:
- Novo campo `ai_suggested_category: ReportCategory | None = None` (opcional, nasce `None`).

**DB model** — `infrastructure/database/models.py`:
- Coluna `ai_suggested_category = Column(SAEnum(ReportCategory), nullable=True)`.

**Repository ABC** — `domain/repositories/security_report_repository.py`:
- `update_ai_suggested_category(id, category)` — salva sugestão sem alterar `category` confirmada.
- `update_category(id, category)` — atualiza `category` e zera `ai_suggested_category`.

**SQLAlchemy repo** — `infrastructure/repositories/sqlalchemy_security_report_repository.py`:
- Implementação dos dois novos métodos.
- `_to_entity` e `_to_model` atualizados para mapear `ai_suggested_category`.

**Use case `AutoCategorizeReport`** — `application/use_cases/auto_categorize_report.py`:
- `execute(id)` → busca relato; formata `CATEGORIZE_PROMPT`; chama `chat_completion`; parseia JSON; chama `update_ai_suggested_category`; retorna `AutoCategorizeResult(category, confidence, justification)`.
- Levanta `SecurityReportNotFoundError` se relato ausente; `ValueError` se resposta do modelo inválida; `RuntimeError` (repassado) se Ollama inacessível.

**Use case `SetReportCategory`** — `application/use_cases/set_report_category.py`:
- `execute(SetReportCategoryInput(id, category))` → valida `ReportCategory`; chama `update_category`; levanta `InvalidInputError` para categoria inválida, `SecurityReportNotFoundError` para relato ausente.

**Schemas** — `presentation/schemas/security_report_schemas.py`:
- `SecurityReportCategoryUpdate(category: str)` — body do PATCH.
- `AutoCategorizeResponse(category, confidence, justification)` — response do POST auto-categorize.
- `SecurityReportResponse` ganhou `ai_suggested_category: str | None = None`.

**Endpoints** — `presentation/api/routers/security_reports.py`:
- `POST /security_reports/{id}/auto_categorize` → 200 `AutoCategorizeResponse`; 404 se relato ausente; 502 se Ollama falhar ou JSON inválido.
- `PATCH /security_reports/{id}/category` → 200 `SecurityReportResponse`; 404 se relato ausente; 422 se categoria inválida.
- `GET /security_reports/geojson` — propriedade `ai_suggested_category` adicionada ao GeoJSON features.

**Testes**:
- `tests/unit/application/test_auto_categorize.py` — 7 testes unitários com mock de `chat_completion` e repositório.
- `tests/integration/api/test_security_reports_api.py` — 5 novos testes de integração (PATCH /category, POST /auto_categorize com Ollama mocado).

### 0d. Fala Gávea Segurança — ReportCategory enriquecido + seed + AI prompt (plan-000057)

`ReportCategory` expandido de 4 para 9 valores derivados da análise do Fórum de Segurança da Gávea (GaveaLab/PUC-Rio, Jun/2024):

**Enum** — `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py`:
- `FURTO_ROUBO = "furto_roubo"` — Furtos, roubos e assaltos (28% do dataset fake)
- `ILUMINACAO = "iluminacao"` — Problemas de iluminação pública (22%)
- `TRANSITO = "transito"` — Trânsito, acidentes, mobilidade (18%)
- `ESPACO_PUBLICO_INSEGURO = "espaco_publico_inseguro"` — Espaços públicos inseguros (12%)
- `VANDALISMO = "vandalismo"` — Depredação e pichação (8%)
- `MORADORES_SITUACAO_RUA = "moradores_situacao_rua"` — Moradores em situação de rua (5%)
- `CONFLITO_SOCIAL = "conflito_social"` — Conflitos comunitários e tiroteios (4%)
- `BARULHO_PERTURBACAO = "barulho_perturbacao"` — Perturbação da ordem (2%)
- `OUTRO = "outro"` — Residual (1%)

**Seed script** — `fala-gavea-seguranca/scripts/seed_reports.py`: insere 250 relatos com `author_id LIKE 'seed-%'`; idempotente (DELETE antes do INSERT); textos pt-BR em ≥5 variantes por categoria; coordenadas na bbox da Gávea (`lat [-22.990, -22.965], lon [-43.245, -43.215]`); distribuição por `random.choices` com pesos derivados do fórum.

**AI prompt template** — `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/ai/prompts.py`: `CATEGORIZE_PROMPT: str` — template com `/nothink`, 9 categorias descritas em pt-BR, variável `{text}`, instrução de resposta JSON `{category, confidence, justification}`. Preparado para importação por `use_cases/auto_categorize_report.py` (Wave 1 Item 3, roadmap-000056).

### 0e. Fala Gávea Segurança — Filtro temporal `until` (plan-000062)

`ReportFilter` gains a symmetric `until: datetime | None = None` field (sibling of the existing `since`). The SQLAlchemy repository applies `SecurityReportModel.created_at <= filters.until` when set. Both `GET /security_reports/geojson` and `GET /security_reports/` expose `?until=` as an optional query parameter (type `datetime`, parsed by FastAPI).

- **Domain** — `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/repositories/security_report_repository.py`: `ReportFilter.until: datetime | None = None` added after `since`.
- **Infrastructure** — `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/repositories/sqlalchemy_security_report_repository.py`: `find_all()` applies `q.filter(SecurityReportModel.created_at <= filters.until)` after the `since` block.
- **Router** — `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/security_reports.py`: `until: datetime | None = Query(None)` added to `get_geojson` and `list_security_reports`; passed into `ReportFilter(…, until=until, …)`.
- **Tests** — `FakeRepository.find_all` updated to filter by `since`/`until`; `test_filter_since_until_range` and `test_filter_until_only` added (unit); `test_geojson_until_filter` added (integration).

### 0c. Fala Gávea Segurança — Iluminação Pública (plan-000055)

`fala-gavea-seguranca` gained a public-lighting overlay feature. New files:

**Infrastructure loader** — `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/iluminacao/loader.py`:
- `download_iluminacao(cache_path)` — streams the ArcGIS Hub Open Data GeoJSON (`5322126ff10e46249be878ddfd057cc5`) to `fala-gavea-seguranca/data/iluminacao.geojson` via `httpx.stream`. 60-second timeout.
- `load_iluminacao_geojson(cache_path)` — loads the cached file as a Python dict; auto-downloads on first call if cache is absent.
- `_DEFAULT_CACHE` resolves to `fala-gavea-seguranca/data/iluminacao.geojson` via `Path(__file__).parents[4] / "data" / "iluminacao.geojson"`.
- `fala-gavea-seguranca/data/` is gitignored (derived artifact).

**FastAPI router** — `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/iluminacao.py`:
- `GET /iluminacao/geojson` — serves the cached GeoJSON via `JSONResponse`; triggers auto-download on first call; returns 503 on failure.
- `POST /iluminacao/refresh` — schedules a background re-download via FastAPI `BackgroundTasks`; returns 202 immediately.
- Router registered in `main.py` with prefix `/iluminacao`, tag `iluminacao`.

**Leaflet frontend** — `fala-gavea-seguranca/static/app.js`:
- `iluminacaoLayerGroup` (`L.layerGroup()`) + `iluminacaoLoaded` flag added at module level.
- `loadIluminacao()` async function fetches `/iluminacao/geojson` and renders yellow circle markers (`radius: 3, color: '#f0c040'`) onto the layer group via `L.geoJSON`.
- Layer group added to map and loaded on app init; `L.control.layers` wired with `"💡 Luminárias"` toggle (non-collapsed).
- `#btn-refresh-iluminacao` click handler POSTs to `/iluminacao/refresh` and updates `#iluminacao-status` text.

**HTML sidebar** — `fala-gavea-seguranca/static/index.html`:
- Added `#iluminacao-panel` div inside `#sidebar` (after `#filters`) with `#btn-refresh-iluminacao` button and `#iluminacao-status` hint paragraph.

### 0. GaveaLab PoC (sibling project)

`gavealab-poc/` is a Streamlit + Ollama citizen-claims analysis PoC, scaffolded in plan-000008. It runs independently from kb-qa (separate `pyproject.toml`, uv venv). Key components: `GaveaLabWorkspace` (SQLite persistence), `AnalysisSession` (domain object), `gavealab_poc/llm.py` (Ollama OpenAI-compatible wrapper), and page modules for upload (plan-000009), auto-topics, manual-topics, and cruxes (stubs).

**Navigation (plan-000021)**: `app.py` uses `st.navigation()` + `st.Page()` (Streamlit 1.28+ API). Six pages are defined as zero-arg wrapper functions that call `render(get_workspace())`. "Todos os Estudos" is the default landing page. A sidebar indicator shows the active session name (or "Nenhuma sessao ativa."). The old `st.sidebar.radio` dispatch block is removed.

**All-studies dashboard (plan-000021)**: `gavealab_poc/pages/all_sessions.py` implements the "Todos os Estudos" page. Calls `workspace.get_sessions_summary()` (new method — two SQL queries: sessions + result types; `comment_count` approximated from newline count in `csv_raw`). Renders each session as a bordered `st.container` with two columns: name/date/comment-count on the left, four `st.badge()` status indicators on the right (Temas, Claims, Divergencias, Categorias — green when the result exists, gray otherwise; UMAP badge green when `claims_tree` present). An "Abrir este estudo" button loads the session into `st.session_state.session` and calls `st.rerun()`.

**Upload page (plan-000009, updated plan-000021)**: `gavealab_poc/pages/upload.py` implements the CSV upload flow: file picker, session name input, 10-row preview via pandas, validation, session creation via `workspace.create_session()`. The "Sessoes anteriores" inline panel was removed (plan-000021) — session management is now owned by the "Todos os Estudos" page. A `st.info()` hint directs users to that page.

**Auto-topics page (plan-000010)**: `gavealab_poc/pages/auto_topics.py` renders the "Temas automaticos" page. A "Gerar temas com IA" button triggers `generate_topic_tree(session)` from `gavealab_poc/pipeline/topics.py`, which assembles all comments (≥10 chars) from `session.df["text"]`, calls Ollama via `llm.chat()` with a structured JSON prompt, parses the response with `_parse_taxonomy` / `_extract_json` (best-effort JSON extraction with `{...}` block fallback), and persists the result via `session.save_result("topic_tree", tree)`. The page then renders each topic as a `st.expander` with subtopics listed as markdown bullet points. Results survive page reload (loaded from SQLite via `AnalysisSession.topic_tree`).

**Manual theme categorization (plan-000012)**: `gavealab_poc/pipeline/manual_categories.py` adds `categorize_by_themes(session, themes)`, which iterates over `session.df["text"]` (≥10 chars), calls `llm.chat()` per comment with a prompt listing user-supplied themes, and parses matches via `_parse_theme_matches` (reusing `_extract_json` from `pipeline/topics.py`). Each matching entry carries `id`, `text`, optionally `territory` (when the column exists), and `reason`. Results are accumulated into `{theme_name: [entry, ...]}` and persisted via `session.save_result("manual_categories", result)`. The manual_topics page (`gavealab_poc/pages/manual_topics.py`) replaces the stub: a `st.text_area` collects one theme per line; a "Categorizar relatos" button triggers categorization; results are shown per-theme in `st.expander` blocks as dataframes with columns `territory` (when present), `text`, and `reason`.

**Claims extraction (plan-000011)**: `gavealab_poc/pipeline/claims.py` adds `extract_claims(session)`, which iterates over every comment in `session.df["text"]` (≥10 chars), calls `llm.chat()` with a per-comment prompt that includes the full topic/subtopic taxonomy as JSON, and parses each response with `_parse_claims` (reusing `_extract_json` from `pipeline/topics.py`). Each claim dict carries `claim`, `quote`, `topicName`, `subtopicName`, `commentId`, and `territory` (when the column exists in the DataFrame). Results are accumulated into a nested dict `{topicName: {subtopicName: [claim_dict, ...]}}` and persisted via `session.save_result("claims_tree", result)`. The auto_topics page exposes a "Extrair claims" button below the topic tree; the resulting claims are rendered per-subtopic in `st.expander` blocks as dataframes (columns: `claim`, `quote`, and optionally `territory`).

**UMAP cluster visualization (plan-000016)**: `gavealab-poc/gavealab_poc/pipeline/umap_viz.py` provides `build_umap_df(claims_tree, n_neighbors, min_dist)`, which flattens the nested claims tree into rows, calls `embed()` for L2-normalised embeddings, and runs `umap.UMAP` (cosine metric, `random_state=42`, `n_neighbors` clamped to `min(value, N-1)` to avoid crash on tiny datasets). Returns a DataFrame with columns `x, y, claim, topic, subtopic, territory`. The page `gavealab_poc/pages/umap_viz.py` renders a `st.form`-gated Plotly scatter chart (color by territory, hover shows claim + subtopic, Pastel color scale, height 600px) plus an expandable data table. Sliders for `n_neighbors` (2–50) and `min_dist` (0.01–0.5) use `st.form` so UMAP only reruns on explicit "Gerar visualizacao" submit. Dependencies `umap-learn>=0.5` and `plotly>=5.0` added to `gavealab-poc/pyproject.toml`. The "Visualizar clusters" option added to the `app.py` sidebar radio.

**Divergent opinion detection / cruxes (plan-000013)**: `gavealab_poc/embeddings.py` provides a singleton `SentenceTransformer` (`intfloat/multilingual-e5-large`, 560MB, cached via `lru_cache`) and an `embed(texts, prefix)` helper that returns L2-normalised embeddings as a NumPy array. `gavealab_poc/pipeline/cruxes.py` implements `detect_cruxes(session)` using a three-step pipeline: (1) embed each claim with `"passage: "` prefix; (2) per subtopic, compute centroid embedding per territory group; (3) if cosine distance between centroids exceeds `DIVERGENCE_THRESHOLD = 0.25`, call Ollama (`llm.chat()`) for a one-sentence crux label (up to 3 retries for JSON parse failures). Only divergent subtopics trigger an LLM call. Results are persisted via `session.save_result("cruxes", cruxes)`, where each crux dict carries `topic`, `subtopic`, `cruxClaim`, `explanation`, `agree`, `disagree`, and `cosine_distance`. The cruxes page (`gavealab_poc/pages/cruxes.py`) replaces the stub: a "Detectar divergencias" button triggers detection; results are shown as `st.expander` cards with topic/subtopic label, cosine distance, crux claim, and two-column Concordam/Discordam layout. Dependencies `sentence-transformers>=3.0` and `numpy>=1.26` added to `gavealab-poc/pyproject.toml`.

### 1. Platform Purpose

kb-qa is a local RAG knowledge base CLI and MCP server. It ingests `.md` and `.pdf` documents from `knowledge/` into a ChromaDB vector store, and exposes semantic search via the `query_knowledge` MCP tool and the `kb-qa ask` CLI command.

#### Design Philosophy

Privacy-first local RAG. All compute (embedding, storage, retrieval) runs on the local machine. No cloud dependency except the AI client that consumes the MCP tool.

### 2. Entity Hierarchy

```
KnowledgeDocument  (.md or .pdf in knowledge/)
└── Chunk          (text segment with metadata, stored in ChromaDB)

VectorStore        (ChromaDB PersistentClient, knowledge/vectorstore/, collection: kb-qa-docs)
```

#### KnowledgeDocument

Source files in `knowledge/`. Loaded by `src/kb_qa/loader.py` (`load_all()`). Supported types: `md` (Markdown), `pdf` (pymupdf). Not persisted directly — only Chunks derived from them are indexed.

#### Chunk

`TypedDict` (`Document` in `src/kb_qa/loader.py`): `{"text": str, "metadata": {"type": str, "name": str, "source": str}}`. ID: MD5 of `source + text[:200]` (computed in `src/kb_qa/ingest.py:_doc_id()`). Cosine embeddings stored in ChromaDB collection `kb-qa-docs`.

### 3. Domain-Specific Concepts

**Content-addressable ingestion**: `_doc_id()` computes MD5 of `source::text[:200]`. Existing IDs are skipped on re-ingest (unless `--force`). Implemented in `src/kb_qa/ingest.py`.

**Embedding model**: `nomic-ai/nomic-embed-text-v1` via `SentenceTransformer`. Loaded fresh per CLI invocation; session-reuse wrapper `KbQa` exists in `src/kb_qa/query.py` but is not yet used by the CLI.

**Cosine similarity search**: ChromaDB collection created with `{"hnsw:space": "cosine"}`. Queries use `collection.query(query_embeddings=[...], n_results=N)`.

**MCP boundary**: FastMCP server in `agents/mcp_server.py`. Single tool: `query_knowledge(question, n_results=5, doc_type=None)`. Cap: `n_results = min(n_results, 20)`.

### 4. Permission Model

#### System-Level Roles

| Role | Level | Capabilities |
|------|-------|-------------|
| Local user | — | Full access: ingest, status, ask, MCP query |

No authentication. Local filesystem is the access control layer.

### 5. Content Authoring & Attribution

Not implemented. Documents are user-managed files in `knowledge/`.

### 6. Content Import / Export

Ingestion only: `.md` (Markdown loader) and `.pdf` (pymupdf loader) via `src/kb_qa/loader.py`. No export.

### 7. User Community & Localization

CLI interface: English. Knowledge documents: any language (multilingual embedding model). No i18n framework.

### 8. UX Patterns

CLI commands: `ingest` (with progress bar), `status` (chunk counts + delta), `ask` (retrieval + text truncation at 500 chars per chunk).

### 9. Administrative Domain

No activity logging. No backup/restore. Vector store rebuilt by running `kb-qa ingest`.

### 10. Validation Constants

| Constant | Value | Defined in |
|----------|-------|-----------|
| `n_results` max (MCP) | 20 | `agents/mcp_server.py` |
| `EMBED_BATCH_SIZE` | 256 | `src/kb_qa/constants.py` |
| `DOCUMENT_TYPES` | `{"md", "pdf"}` | `src/kb_qa/constants.py` |
| `COLLECTION_NAME` | `kb-qa-docs` | `src/kb_qa/constants.py` |
| `EMBED_MODEL` | `nomic-ai/nomic-embed-text-v1` | `src/kb_qa/constants.py` |

---

## Metacommunication

> Populated by post-skill after first plan execution.

---

## Journey Maps

> Populated by post-skill after first plan execution.
