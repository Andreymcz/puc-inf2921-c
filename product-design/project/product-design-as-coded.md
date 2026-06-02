---
designer_description: "Implementation state mirror for kb-qa — maintained by post-skill after each plan execution."
---

# AS-CODED — INF2921-Grupo-C / kb-qa

<!-- maintained-by: Agent (post-skill); Agent classification since SEJA 2.8.4 -->

---

## Conceptual Design

### 0. GaveaLab PoC (sibling project)

`gavealab-poc/` is a Streamlit + Ollama citizen-claims analysis PoC, scaffolded in plan-000008. It runs independently from kb-qa (separate `pyproject.toml`, uv venv). Key components: `GaveaLabWorkspace` (SQLite persistence), `AnalysisSession` (domain object), `gavealab_poc/llm.py` (Ollama OpenAI-compatible wrapper), and page modules for upload (plan-000009), auto-topics, manual-topics, and cruxes (stubs).

**Upload page (plan-000009)**: `gavealab_poc/pages/upload.py` implements the full CSV upload flow: file picker, session name input, 10-row preview via pandas, validation (column presence enforced by `workspace._parse_csv`), session creation via `workspace.create_session()`, and a "Sessoes anteriores" panel listing and reloading persisted sessions from SQLite.

**Auto-topics page (plan-000010)**: `gavealab_poc/pages/auto_topics.py` renders the "Temas automaticos" page. A "Gerar temas com IA" button triggers `generate_topic_tree(session)` from `gavealab_poc/pipeline/topics.py`, which assembles all comments (≥10 chars) from `session.df["text"]`, calls Ollama via `llm.chat()` with a structured JSON prompt, parses the response with `_parse_taxonomy` / `_extract_json` (best-effort JSON extraction with `{...}` block fallback), and persists the result via `session.save_result("topic_tree", tree)`. The page then renders each topic as a `st.expander` with subtopics listed as markdown bullet points. Results survive page reload (loaded from SQLite via `AnalysisSession.topic_tree`).

**Manual theme categorization (plan-000012)**: `gavealab_poc/pipeline/manual_categories.py` adds `categorize_by_themes(session, themes)`, which iterates over `session.df["text"]` (≥10 chars), calls `llm.chat()` per comment with a prompt listing user-supplied themes, and parses matches via `_parse_theme_matches` (reusing `_extract_json` from `pipeline/topics.py`). Each matching entry carries `id`, `text`, optionally `territory` (when the column exists), and `reason`. Results are accumulated into `{theme_name: [entry, ...]}` and persisted via `session.save_result("manual_categories", result)`. The manual_topics page (`gavealab_poc/pages/manual_topics.py`) replaces the stub: a `st.text_area` collects one theme per line; a "Categorizar relatos" button triggers categorization; results are shown per-theme in `st.expander` blocks as dataframes with columns `territory` (when present), `text`, and `reason`.

**Claims extraction (plan-000011)**: `gavealab_poc/pipeline/claims.py` adds `extract_claims(session)`, which iterates over every comment in `session.df["text"]` (≥10 chars), calls `llm.chat()` with a per-comment prompt that includes the full topic/subtopic taxonomy as JSON, and parses each response with `_parse_claims` (reusing `_extract_json` from `pipeline/topics.py`). Each claim dict carries `claim`, `quote`, `topicName`, `subtopicName`, `commentId`, and `territory` (when the column exists in the DataFrame). Results are accumulated into a nested dict `{topicName: {subtopicName: [claim_dict, ...]}}` and persisted via `session.save_result("claims_tree", result)`. The auto_topics page exposes a "Extrair claims" button below the topic tree; the resulting claims are rendered per-subtopic in `st.expander` blocks as dataframes (columns: `claim`, `quote`, and optionally `territory`).

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
