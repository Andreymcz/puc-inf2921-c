---
designer_description: "Engineering standards for INF2921-Grupo-C — GaveaLab (Streamlit) primary product and kb-qa (CLI/MCP) supporting tool."
---

# ENGINEERING STANDARDS — INF2921-Grupo-C / GaveaLab + kb-qa

> **Primary product stack**: Python 3.13 · Streamlit · SQLite · Ollama (OpenAI-compatible) · sentence-transformers · UMAP · Plotly · uv
>
> **Supporting tool stack**: Python 3.13 · click · ChromaDB · sentence-transformers · FastMCP · pymupdf · uv

---

## Backend

### 1. Project Structure

```
src/kb_qa/
├── __init__.py          # Package version
├── __main__.py          # Entry point (python -m kb_qa)
├── cli.py               # Click CLI group and commands
├── constants.py         # All project-wide constants (model name, paths, batch size)
├── loader.py            # Document loading: load_all(), Document TypedDict
├── ingest.py            # Ingestion pipeline: ingest(), _doc_id()
└── query.py             # Retrieval: retrieve(), KbQa session-reuse class

agents/
└── mcp_server.py        # FastMCP server exposing query_knowledge tool

tests/
├── conftest.py          # Shared fixtures
└── test_*.py            # Test modules

knowledge/               # Source documents (.md, .pdf) — user-managed
  vectorstore/           # ChromaDB database — gitignored, derived artifact
```

**Rules:**
- `constants.py` is the single source of truth for model name, paths, batch size, collection name.
- `loader.py` owns document loading and chunking. No file I/O elsewhere.
- `ingest.py` owns embedding and upsert logic. No direct ChromaDB access in `cli.py`.
- `query.py` owns retrieval logic. The `KbQa` class provides session reuse (model + collection loaded once).
- `cli.py` is the HTTP-agnostic CLI layer — it calls functions from ingest/query, never touches ChromaDB directly.
- `mcp_server.py` is the MCP adapter layer — it delegates to `query.py`, no business logic.

---

### 2. Module Responsibilities

| Module | Responsibility | May import |
|--------|---------------|-----------|
| `cli.py` | Click commands, user feedback | `ingest`, `query`, `constants`, `loader` |
| `ingest.py` | Load → embed → upsert pipeline | `loader`, `constants`, chromadb, sentence_transformers |
| `query.py` | Embed query → cosine search → return chunks | `constants`, chromadb, sentence_transformers |
| `loader.py` | Load .md and .pdf files, return Document list | pathlib, pymupdf |
| `constants.py` | Path and model constants | pathlib only |
| `mcp_server.py` | FastMCP tool wrapper | `query`, mcp |

---

### 3. Constants Policy

All configurable values live in `src/kb_qa/constants.py`. Inline literals for model names, collection names, or numeric limits are prohibited in business logic.

```python
# constants.py
KNOWLEDGE_DIR: Path = Path(__file__).parent.parent.parent / "knowledge"
VECTORSTORE_DIR: Path = KNOWLEDGE_DIR / "vectorstore"
COLLECTION_NAME: str = "kb-qa-docs"
EMBED_MODEL: str = "nomic-ai/nomic-embed-text-v1"
DOCUMENT_TYPES: frozenset[str] = frozenset({"md", "pdf"})
EMBED_BATCH_SIZE: int = 256
```

---

### 4. Type Annotations

All public functions and methods must have complete type annotations. Private helpers (`_doc_id`, `_load_pdf`, etc.) should be annotated where the type is non-obvious.

```python
def retrieve(
    question: str,
    n_results: int = 5,
    vectorstore_dir: Path = VECTORSTORE_DIR,
    doc_type_filter: str | None = None,
) -> list[Document]:
    ...
```

---

### 5. Logging

Use module-level loggers. No `print()` for operational messages.

```python
import logging
log = logging.getLogger(__name__)

log.info("Ingested %d new chunks", count)
log.warning("No documents found in %s", knowledge_dir)
```

| Level | When to use |
|-------|-------------|
| `DEBUG` | Detailed diagnostics (disabled in production) |
| `INFO` | Normal operational events (ingestion progress, chunk counts) |
| `WARNING` | Unexpected but recoverable situations |
| `ERROR` | Failures affecting the current operation |

The CLI configures `logging.basicConfig(level=logging.INFO)` in the `ingest` command. Other commands do not configure logging unless needed.

---

### 6. Naming Conventions

| Category | Convention | Examples |
|----------|-----------|---------|
| Modules | `snake_case.py` | `ingest.py`, `loader.py` |
| Classes | `PascalCase` | `KbQa` |
| Functions | `snake_case` | `retrieve`, `load_all`, `_doc_id` |
| Constants | `UPPER_SNAKE_CASE` | `EMBED_MODEL`, `COLLECTION_NAME` |
| Test files | `test_<module>.py` | `test_ingest.py`, `test_query.py` |
| Private helpers | `_snake_case` | `_doc_id`, `_load_pdf` |

---

### 7. Dependency Management

**Tool:** `uv` with `pyproject.toml` + `uv.lock`.

```toml
[project]
requires-python = ">=3.13"
dependencies = [
    "chromadb>=0.5",
    "sentence-transformers>=3.0",
    "pymupdf>=1.24",
    "mcp[cli]>=1.0",
    "anthropic>=0.40",
    "click>=8.0",
    "einops>=0.8.2",
]

[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "ruff", "pyright"]
```

**Rules:**
- Use ranges (`>=X.Y`) in `pyproject.toml`; `uv.lock` pins exact versions.
- Production deps separated from dev deps via `[project.optional-dependencies]`.
- `uv sync` installs all deps including dev; `uv sync --no-dev` for production-only.
- Review and update dependencies after each ChromaDB or sentence-transformers major release.

---

### 8. Error Handling

- CLI commands catch `Exception` at the boundary and emit user-friendly messages via `click.echo(..., err=True)`.
- MCP tool catches `Exception` and returns `[{"error": str(e)}]` — never raises into the MCP runtime.
- Internal functions raise typed exceptions; the adapter layer (cli.py, mcp_server.py) catches and translates.

---

## Testing

### 1. Backend Testing (pytest)

#### Stack

| Tool | Purpose |
|------|---------|
| pytest | Test runner |
| pytest-cov | Coverage reporting |
| tmp_path fixture | Isolated temporary directories for vector stores in tests |

#### Test Pattern

```python
def test_ingest_creates_chunks(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "test.md").write_text("# Hello\n\nWorld")
    vectorstore_dir = tmp_path / "vectorstore"

    count = ingest(knowledge_dir=knowledge_dir, vectorstore_dir=vectorstore_dir)
    assert count > 0
```

#### Fixtures (conftest.py)

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `tmp_knowledge_dir` | function | Temporary knowledge/ with sample .md and .pdf fixtures |
| `tmp_vectorstore_dir` | function | Isolated vectorstore dir (separate from production) |
| `sample_chunks` | function | Pre-built list of Document dicts for retrieval tests |

#### Rules

- Use `tmp_path` (pytest built-in) for all filesystem operations in tests — never read/write `knowledge/vectorstore/` in tests.
- Mock `SentenceTransformer.encode` in unit tests to avoid downloading the model in CI.
- Test both success and error paths: missing knowledge dir, empty collection, unsupported file type.
- File naming: `test_<module>.py` (e.g., `test_ingest.py`, `test_query.py`, `test_loader.py`).

---

## i18n

**kb-qa**: Not applicable. CLI and MCP tool are English-only. Knowledge documents may be in any language.

**GaveaLab**: UI labels, sidebar navigation, page titles, and all LLM prompts are in pt-BR. Code and error messages are in English. No i18n framework — strings are inline in Streamlit components and prompt templates. The embedding model handles multilingual content without additional configuration.

---

## GaveaLab-Specific Standards

### Directory Layout

```
gavealab-poc/
  app.py                        # Streamlit entry point — only page dispatch and workspace init
  gavealab_poc/
    __init__.py
    llm.py                      # OllamaClient — all LLM calls go here
    workspace.py                # GaveaLabWorkspace + AnalysisSession — all SQLite access goes here
    embeddings.py               # Embedding computation (sentence-transformers)
    pipeline/
      topics.py                 # Step 1: comments → topic tree
      claims.py                 # Step 2: comments + tree → claims
      cruxes.py                 # Step 3: claims → crux analysis
      manual_categories.py      # Step 4 (alt): manual theme categorization
      umap_viz.py               # UMAP projection of claim embeddings
    pages/
      upload.py                 # Page: CSV upload + session management
      auto_topics.py            # Page: auto topic analysis
      manual_topics.py          # Page: manual theme categorization
      cruxes.py                 # Page: divergence view
      umap_viz.py               # Page: UMAP cluster visualization
  pyproject.toml                # dependencies: streamlit, pandas, sentence-transformers, umap-learn, plotly
```

### Module Responsibilities

| Module | Responsibility | May import |
|--------|---------------|-----------|
| `app.py` | Page dispatch, `@st.cache_resource` workspace | `workspace`, `pages.*` |
| `llm.py` | `OllamaClient` — POST to Ollama, parse JSON, return structured output | httpx or openai |
| `workspace.py` | `GaveaLabWorkspace` (SQLite), `AnalysisSession` (dataclass) | sqlite3, pandas |
| `embeddings.py` | `embed_claims()` — batch embedding via sentence-transformers | sentence_transformers |
| `pipeline/*.py` | Stateless pipeline steps — accept session data, return structured results | `llm`, `workspace` (read), `embeddings` |
| `pages/*.py` | Streamlit page render — call pipeline, call `session.save_result()`, display results | `pipeline.*`, `workspace` |

### Streamlit Conventions

- `@st.cache_resource` is used **only** for `GaveaLabWorkspace` (singleton across rerenders). Never use it for pipeline results — those live in the session via `st.session_state`.
- Long-running LLM calls must be wrapped in `with st.spinner("...")` to provide user feedback.
- Each page module exports a single `render(workspace: GaveaLabWorkspace) -> None` function. No Streamlit calls outside this function.
- `st.session_state.session` holds the active `AnalysisSession` (or `None` if no session loaded). All pages check for `None` and redirect to upload page if no session is active.

### SQLite Schema

```sql
CREATE TABLE sessions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    csv_raw    TEXT NOT NULL,
    created_at TEXT NOT NULL          -- ISO-8601 UTC
);
CREATE TABLE results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL REFERENCES sessions(id),
    result_type TEXT NOT NULL,        -- 'topic_tree' | 'claims_tree' | 'cruxes' | 'manual_categories'
    result_json TEXT NOT NULL,        -- JSON blob
    created_at  TEXT NOT NULL
);
```

`GaveaLabWorkspace.save_result()` deletes and reinserts on re-run (upsert semantics). This is intentional — only one result per `(session_id, result_type)` is kept.

### LLM Pipeline Conventions

- All pipeline functions are **pure** with respect to the database: they accept data as arguments and return structured Python objects. `save_result()` is called by the **page** module, not the pipeline module.
- Prompts are defined as module-level constants (not inline strings) in each `pipeline/*.py` file.
- LLM responses are always parsed as JSON. If parsing fails, pipeline functions raise a descriptive `ValueError` rather than returning partial data.
- Thinking mode is disabled (`/nothink` or equivalent) for speed in interactive sessions.

### Error Handling

- Page modules catch `Exception` from pipeline calls and display `st.error(str(e))` — never let exceptions surface as Streamlit tracebacks to the user.
- `OllamaClient` raises `RuntimeError` if Ollama is unreachable, with a message that includes the configured URL, so the user knows what to check.
- `GaveaLabWorkspace` raises `ValueError` for missing sessions with a descriptive message.
