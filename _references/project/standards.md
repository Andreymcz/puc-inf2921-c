# ENGINEERING STANDARDS — INF2921 Grupo C

---

## Backend

### 1. Project Structure

```
src/kb_qa/
├── __init__.py
├── __main__.py
├── cli.py          # Click CLI entry point
├── constants.py    # Shared constants (collection name, chunk size, etc.)
├── ingest.py       # Document ingestion pipeline
├── loader.py       # File loaders (.md, .pdf)
└── query.py        # RAG query logic

agents/
├── __init__.py
└── mcp_server.py   # MCP server exposing query_knowledge tool

knowledge/
└── vectorstore/    # ChromaDB persistence (not committed to git)

tests/
├── conftest.py
└── test_*.py
```

### 2. Module Responsibilities

- **cli.py**: Click commands only — delegates all logic to ingest.py and query.py
- **ingest.py**: Load → chunk → embed → store. Single write path to ChromaDB.
- **loader.py**: File-type dispatch (Markdown via plain read, PDF via PyMuPDF)
- **query.py**: Embed query → similarity search → return ranked chunks
- **constants.py**: Collection name, chunk size, overlap, model name, top-k default
- **mcp_server.py**: MCP transport wrapper around query.py — no direct ChromaDB access

### 3. Coding Conventions

- Python 3.13, typed with `pyright` (strict mode disabled, but type hints required on public functions)
- Line length: 100 (ruff)
- Imports sorted by ruff (isort-compatible)
- No raw ChromaDB calls outside `ingest.py` and `query.py`

### 4. Dependencies

Managed via `pyproject.toml` + `uv`. Production deps in `[project.dependencies]`, dev deps in `[project.optional-dependencies] dev`.

### 5. Error Handling

- CLI errors: print user-friendly message via Click, exit with non-zero code
- MCP errors: return structured error response per MCP spec
- No bare `except:` clauses — catch specific exceptions

---

## Frontend

N/A — no frontend.

---

## Testing

### 1. Framework

- **Backend**: pytest with pytest-cov
- **Frontend**: N/A
- **E2E**: N/A

### 2. Test Location

All tests in `tests/`. Test files named `test_<module>.py`.

### 3. Running Tests

```bash
uv run pytest                    # all tests
uv run pytest tests/test_ingest.py  # single file
uv run pytest --cov=src/kb_qa   # with coverage
```

### 4. Fixtures

Shared fixtures in `tests/conftest.py`. Use a temporary ChromaDB directory for isolation:

```python
@pytest.fixture
def tmp_store(tmp_path):
    # ChromaDB client pointing at tmp_path
    ...
```

### 5. Coverage Target

80% line coverage for `src/kb_qa/` modules.

---

## i18n

No runtime i18n. Documents ingested may be in pt-BR or en-US. No translation catalogs required.
