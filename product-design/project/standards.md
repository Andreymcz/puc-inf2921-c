---
designer_description: "Engineering standards for kb-qa — Python CLI/MCP library project conventions, testing, logging, and dependency management."
---

# ENGINEERING STANDARDS — INF2921-Grupo-C / kb-qa

> **Stack**: Python 3.13 · click · ChromaDB · sentence-transformers · FastMCP · pymupdf · uv
>
> This is a CLI/library project with no web framework and no frontend. Web-specific sections (HTTP, auth, CSRF, ORM, migrations, frontend) are intentionally omitted.

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

Not applicable. The CLI interface and MCP tool are English-only. Knowledge documents may be in any language — the embedding model (`nomic-ai/nomic-embed-text-v1`) handles multilingual content without additional configuration. No i18n framework is used.
