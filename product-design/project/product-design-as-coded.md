---
designer_description: "Implementation state mirror for kb-qa — maintained by post-skill after each plan execution."
---

# AS-CODED — INF2921-Grupo-C / kb-qa

<!-- maintained-by: Agent (post-skill); Agent classification since SEJA 2.8.4 -->

---

## Conceptual Design

### 0b. Fala Gávea — Streamlit frontend (plan-000030, plan-000033)

`fala-gavea/app.py` is a single-file Streamlit app that consumes the Fala Gávea FastAPI backend (`fala-gavea/src/`). The API base URL defaults to `http://localhost:8000`, overridable via `FALA_GAVEA_API_URL`. A `user_id` UUID is generated once per session and stored in `st.session_state`.

**Four pages** (dispatched via sidebar radio):
- **📋 Postagens**: lists all posts with like counter; clicking ❤️ toggles a like. When `likes_count > 0`, a `st.expander("Ver quem curtiu")` appears — on expansion it calls `GET /citizen_posts/{id}/likes` and lists liker `user_id`s.
- **✍️ Nova Postagem**: form to create a new post (text + territory level/name); calls `POST /citizen_posts/`.
- **🏷️ Validar Labels**: shows posts that have `ai_labels`; per-label 👍/👎 buttons call `POST /citizen_posts/{id}/label_feedback`. Vote state reads from `label_feedback[label]["approved"]` (new dict structure).
- **📊 Dashboard**: summary metrics, top-10 posts by likes, bar chart of posts by territory, label feedback summary table, and two new traceability subsections: "Rastreabilidade de likes" (on-demand bulk fetch via "Carregar rastreabilidade" button — shows post_id, text, likers) and "Rastreabilidade de labels" (reads `label_feedback` dict — shows label, aprovado, usuario).

**API helpers**: `api_get(path, **params)` and `api_post(path, body)` call the backend synchronously via `httpx` with a 10-second timeout and raise on 4xx/5xx.

**Like and label traceability (plan-000033)**:
- `GET /citizen_posts/{id}/likes` returns `PostLikesResponse{post_id, likers: [{user_id, created_at}]}` — implemented by `GetPostLikes` use case and `SQLAlchemyCitizenPostRepository.get_likes`.
- `label_feedback` JSON column stores `{label: {"approved": bool, "user_id": str}}` — `set_label_feedback` persists `user_id` alongside the flag.
- `LikeRecord` domain dataclass: `user_id: str, created_at: datetime`. `CitizenPostRepository` exposes `get_likes(post_id) -> list[LikeRecord]`.

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
