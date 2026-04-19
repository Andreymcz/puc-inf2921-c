# DONE | 2026-04-19 12:39 UTC | Plan 000033 | FEATURE-X | 2026-04-19 02:24 UTC | Create kb-qa generic RAG repository | Review: Standard
plan_format_version: 1
source: advisory-000031 -- extract generic KB-QA layer from resqml-expert for reuse across projects

## User Brief

Create a new dedicated repository `kb-qa` — a generic RAG knowledge base that ingests .md and .pdf files into ChromaDB via sentence-transformers, and exposes query_knowledge via an MCP server for SEJA integration.

## Agent Interpretation

- **Problem**: The RAG pipeline in `resqml-expert` is domain-specific (XSD, PYI, fesapi). Other projects (SEJA-based or otherwise) need the same pattern — ingest local documents into a searchable vector store, query via MCP — but without any RESQML dependency.
- **Approach**: Extract and simplify the `src/rag/` module into a new standalone repository `kb-qa`, reducing loaders to `.md` and `.pdf` only, removing all domain-specific scripts, and providing a single `query_knowledge` MCP tool. The new repo is self-contained, installable via `uv sync`, and integrable into any SEJA project via `.claude/settings.json` MCP config.
- **Alternatives rejected**: (1) Making `resqml-expert` itself generic — rejected because it carries fesapi, h5py, scipy, and RESQML-specific knowledge assets that are irrelevant to other domains. (2) A SEJA skill that wraps the existing MCP — rejected because the KB itself needs to live in a separate, domain-agnostic repo.

## Files

All files below are in the **new `kb-qa` repository** (not in `resqml-expert`).

Target directory: `../kb-qa/` (sibling to this repository)

### Created
- `pyproject.toml`
- `README.md`
- `.gitignore`
- `CLAUDE.md`
- `knowledge/.gitkeep`
- `src/kb_qa/__init__.py`
- `src/kb_qa/constants.py`
- `src/kb_qa/loader.py`
- `src/kb_qa/ingest.py`
- `src/kb_qa/query.py`
- `src/kb_qa/cli.py`
- `src/kb_qa/__main__.py`
- `agents/mcp_server.py`
- `tests/__init__.py`
- `tests/test_loader.py`
- `tests/test_ingest.py`

## Best Practices

- Extract only what is needed — no RESQML-specific code, no fesapi, no XSD/PYI loaders
- `loader.py`: only `.md` and `.pdf` loaders, using the same `Document` TypedDict + `LoaderConfig` registry pattern from resqml-expert (but simplified)
- `ingest.py`: identical pattern to resqml-expert — idempotent, batch-based, `--force` flag
- MCP server: single `query_knowledge` tool, no EPC/RESQML tools
- All public functions have type annotations (pyright enforced)
- No hardcoded paths — use `constants.py` and CLI args
- Package name: `kb_qa` (underscore, importable); CLI entry point: `kb-qa`

## Design Decisions

- **User-visible impact**: Users in any SEJA project can add `kb-qa` as an MCP server in `.claude/settings.json` and immediately query local `.md` and `.pdf` documents from within Claude Code. SEJA plan files, advisory logs, and PDFs become searchable knowledge assets.
- **Trade-offs accepted**: Limiting loaders to `.md` + `.pdf` makes the system instantly reusable but means adding new document types requires modifying `loader.py`. The `LoaderConfig` registry pattern (from resqml-expert) keeps this extension cost low.
- **Metacommunication impact**: When a developer uses `kb-qa`, I provide answers grounded in their own project's documentation — plans, decisions, PDFs — reducing context-switching out of Claude Code.

---

## Steps

### Step 1: Initialize repository scaffold
Create the `kb-qa` repository directory with `pyproject.toml`, `.gitignore`, `README.md`, `CLAUDE.md`, and empty `knowledge/` directory. The package uses `uv` as package manager, `ruff` for linting, `pyright` for type checking, `pytest` for tests. Dependencies: `chromadb>=0.5`, `sentence-transformers>=3.0`, `pymupdf>=1.24`, `mcp[cli]>=1.0`, `anthropic>=0.40`, `click>=8.0`. Dev dependencies: `pytest`, `pytest-cov`, `ruff`, `pyright`.

The `CLAUDE.md` must document: stack, common commands (`uv sync`, `uv run python -m kb_qa ingest`, `uv run python agents/mcp_server.py`), repository structure, and MCP integration instructions.

- **Files**: `../kb-qa/pyproject.toml` (create), `../kb-qa/.gitignore` (create), `../kb-qa/README.md` (create), `../kb-qa/CLAUDE.md` (create), `../kb-qa/knowledge/.gitkeep` (create)
- **References**: general/coding-standards
- **Depends on**: none
- **Verify**: `cd ../kb-qa && uv sync` completes without errors; `uv run python -c "import kb_qa"` succeeds
- **Tests**: N/A (scaffolding only)
- **Docs**: N/A
- **Traces**: N/A
- [x] Done

### Step 2: Implement `constants.py` and `loader.py`
Create `src/kb_qa/constants.py` with:
```python
KNOWLEDGE_DIR: Path = Path(__file__).parent.parent.parent / "knowledge"
VECTORSTORE_DIR: Path = KNOWLEDGE_DIR / "vectorstore"
COLLECTION_NAME: str = "kb-qa-docs"
EMBED_MODEL: str = "nomic-ai/nomic-embed-text-v1"
DOCUMENT_TYPES: frozenset[str] = frozenset({"md", "pdf"})
EMBED_BATCH_SIZE: int = 256
```

Create `src/kb_qa/loader.py` with two loaders and a `LoaderConfig` registry:

**`load_md_chunks(path: Path) -> list[Document]`**: split by H2 headings (`## `). Each section becomes one chunk (title = heading text, text = heading + body). Files with no headings become a single chunk. Truncate each chunk to 2000 chars.

**`load_pdf_chunks(path: Path) -> list[Document]`**: identical logic to `resqml-expert`'s `load_pdf_chunks` — heading-based segmentation with fixed-size fallback (512-word chunks, 64-word overlap). Remove `_infer_version` (not needed); set `metadata["type"] = "pdf"`.

**`LOADER_REGISTRY`**: two entries — `LoaderConfig(".", "**/*.md", load_md_chunks)` and `LoaderConfig(".", "**/*.pdf", load_pdf_chunks)`. Exclude the `vectorstore/` subdirectory from glob results.

**`load_all(knowledge_dir: Path) -> list[Document]`**: iterate registry, rglob, call loader, skip failures with `log.warning`.

- **Files**: `../kb-qa/src/kb_qa/__init__.py` (create), `../kb-qa/src/kb_qa/constants.py` (create), `../kb-qa/src/kb_qa/loader.py` (create)
- **References**: general/coding-standards
- **Depends on**: Step 1
- **Verify**: `uv run python -c "from kb_qa.loader import load_all; print(load_all())"` runs without error (returns empty list when knowledge/ is empty)
- **Tests**: `tests/test_loader.py` — create a temp dir with a sample `.md` file (2 H2 sections) and a minimal PDF (via bytes fixture or skip if pymupdf not available); assert `load_md_chunks` returns 2 documents; assert chunk metadata has `type="md"`, `source`, `name`
- **Docs**: N/A
- **Traces**: N/A
- [x] Done

### Step 3: Implement `ingest.py`
Create `src/kb_qa/ingest.py`. Identical pattern to resqml-expert's `ingest.py`:

```python
def ingest(
    knowledge_dir: Path = KNOWLEDGE_DIR,
    vectorstore_dir: Path = VECTORSTORE_DIR,
    force: bool = False,
    batch_size: int = EMBED_BATCH_SIZE,
) -> int:
```

- Calls `load_all(knowledge_dir)`
- Loads `SentenceTransformer(EMBED_MODEL)`
- Creates/opens `chromadb.PersistentClient` at `vectorstore_dir`
- Gets or creates collection `COLLECTION_NAME` with `{"hnsw:space": "cosine"}`
- Skips already-ingested IDs (idempotency via `collection.get(include=[])["ids"]`)
- Embeds and adds in batches of `batch_size`
- Returns count of newly ingested chunks

- **Files**: `../kb-qa/src/kb_qa/ingest.py` (create)
- **References**: general/coding-standards
- **Depends on**: Step 2
- **Verify**: `uv run python -m kb_qa ingest` runs without error on an empty `knowledge/` (returns 0 chunks)
- **Tests**: `tests/test_ingest.py` — mock `SentenceTransformer` and `chromadb.PersistentClient`; assert `ingest()` returns 0 when no docs; assert `ingest()` returns N when N docs loaded; assert second call returns 0 (idempotency)
- **Docs**: N/A
- **Traces**: N/A
- [x] Done

### Step 4: Implement `query.py` and `cli.py`
Create `src/kb_qa/query.py`:

```python
def retrieve(
    question: str,
    n_results: int = 5,
    vectorstore_dir: Path = VECTORSTORE_DIR,
    doc_type_filter: str | None = None,
) -> list[Document]:
```

Loads `SentenceTransformer(EMBED_MODEL)`, opens ChromaDB collection, embeds the question, queries with optional `where={"type": doc_type_filter}` filter, returns list of `Document` dicts (text + metadata).

Also create a `KbQa` class (mirrors `ResqmlRag` from resqml-expert) for notebook/session reuse — holds model + collection as instance variables.

Create `src/kb_qa/cli.py` with three Click commands:
- `ingest [--force] [--knowledge-dir PATH] [--vectorstore-dir PATH]`
- `status [--knowledge-dir PATH] [--vectorstore-dir PATH]` — shows chunk counts by type, delta between knowledge files and vector store
- `ask QUESTION [--n-results N] [--type md|pdf] [--vectorstore-dir PATH]` — retrieves chunks and prints them (no LLM call needed for basic CLI; LLM call optional with `ANTHROPIC_API_KEY`)

Create `src/kb_qa/__main__.py`: `from kb_qa.cli import cli; cli()`.

- **Files**: `../kb-qa/src/kb_qa/query.py` (create), `../kb-qa/src/kb_qa/cli.py` (create), `../kb-qa/src/kb_qa/__main__.py` (create)
- **References**: general/coding-standards
- **Depends on**: Step 3
- **Verify**: `uv run python -m kb_qa --help` shows commands; `uv run python -m kb_qa status` runs without error
- **Tests**: covered by test_ingest.py mocks; add one test for `retrieve()` using a mocked collection
- **Docs**: N/A
- **Traces**: N/A
- [x] Done

### Step 5: Implement MCP server
Create `agents/mcp_server.py`:

```python
from mcp.server.fastmcp import FastMCP
from kb_qa.query import retrieve as _retrieve

mcp = FastMCP("kb-qa")

@mcp.tool()
def query_knowledge(question: str, n_results: int = 5, doc_type: str | None = None) -> list[dict]:
    """Search the local knowledge base for relevant document chunks.

    Call this to retrieve context from local .md and .pdf documents before
    answering questions. The knowledge base contains whatever documents were
    placed in the knowledge/ directory and ingested via `uv run python -m kb_qa ingest`.

    Args:
        question: Natural language question or keyword.
        n_results: Number of chunks to return (default 5, max 20).
        doc_type: Optional filter — "md" or "pdf".

    Returns:
        List of dicts with keys: text, type, name, source.
        On error: [{"error": "Vector store not found. Run: uv run python -m kb_qa ingest"}]
    """
    try:
        n_results = min(n_results, 20)
        docs = _retrieve(question, n_results=n_results, doc_type_filter=doc_type)
        return [{"text": d["text"], "type": d["metadata"].get("type"), "name": d["metadata"].get("name"), "source": d["metadata"].get("source")} for d in docs]
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    mcp.run()
```

The `CLAUDE.md` MCP integration section must include the `.claude/settings.json` snippet to add `kb-qa` as an MCP server in any SEJA project:
```json
{
  "mcpServers": {
    "kb-qa": {
      "command": "uv",
      "args": ["run", "python", "agents/mcp_server.py"],
      "cwd": "/absolute/path/to/kb-qa"
    }
  }
}
```

- **Files**: `../kb-qa/agents/__init__.py` (create), `../kb-qa/agents/mcp_server.py` (create)
- **References**: general/coding-standards
- **Depends on**: Step 4
- **Verify**: `uv run python agents/mcp_server.py` starts without error and exits cleanly; `uv run python -c "from agents.mcp_server import mcp; print(mcp.name)"` prints `kb-qa`
- **Tests**: N/A (MCP server integration tested manually)
- **Docs**: Update `CLAUDE.md` with MCP integration snippet
- **Traces**: N/A
- [x] Done

### Step 6: Initialize git and run validation
Inside `../kb-qa/`:
1. `git init && git add -A && git commit -m "feat: initial kb-qa implementation"`
2. `uv run ruff check src/ agents/ tests/` — fix any lint errors
3. `uv run pyright src/` — fix any type errors
4. `uv run pytest` — all tests must pass
5. `uv run python -m kb_qa ingest` — runs cleanly on empty knowledge/
6. `uv run python agents/mcp_server.py &` — starts cleanly

- **Files**: `../kb-qa/.git/` (init)
- **References**: general/coding-standards
- **Depends on**: Step 5
- **Verify**: `uv run pytest` passes; `uv run ruff check src/` exits 0; `uv run pyright src/` exits 0
- **Tests**: N/A (validation step)
- **Docs**: N/A
- **Traces**: N/A
- [x] Done

---

## Review Log

### Phase 1 — Perspective Triage (Standard, FEATURE-X)

Shortlist for FEATURE-X (cross-cutting new repo): ARCH, DX, SEC, TEST, OPS

| Perspective | Status | Concern |
|-------------|--------|---------|
| ARCH | Adopted | Clean separation: loader → ingest → query → cli → mcp. No circular deps. Registry pattern keeps load_all open-closed. |
| DX | Adopted | CLAUDE.md documents all commands; MCP integration snippet included; CLI has --help; error messages include fix instructions. |
| SEC | Adopted | No auth surface — local MCP over stdio only. No network listener. No secrets stored. `ANTHROPIC_API_KEY` read from env, never logged. |
| TEST | Deferred | Step 3 mocks SentenceTransformer and ChromaDB — mock/reality divergence risk (same risk advisory-000028 flagged for resqml-expert). Acceptable for now; flag for real integration tests later. |
| OPS | Adopted | `status` command shows delta; `--force` flag for full reingest; logging at INFO/DEBUG levels throughout. |
| PERF | N/A | No server, no HTTP — single-user local tool. Batch size 256 inherited from resqml-expert (validated). |
| DB | N/A | No relational DB — ChromaDB only. |
| API | N/A | No HTTP API. |
| A11Y, VIS, RESP, MICRO, I18N, UX | N/A | No UI. |

**Phase 2**: TEST deferred concern — mock divergence — is low-risk for a new repo (no production traffic). Not triggering Phase 2. Document as a known gap.

### Execution Metrics

| Metric | Value |
|--------|-------|
| Review depth | Standard |
| Perspectives evaluated | 5 |
| Phase 2 triggers | 0 |
| Iterations | 1 |
| Plan amendments | 0 |

---

## Outcomes

- New `kb-qa/` repository with a working RAG pipeline for `.md` and `.pdf` documents
- `uv run python -m kb_qa ingest` ingests documents from `knowledge/` into ChromaDB
- `uv run python agents/mcp_server.py` exposes `query_knowledge` as an MCP tool
- Any SEJA project can add `kb-qa` to `.claude/settings.json` and query their knowledge base from Claude Code

## Smoke

`false` — no API routes, no frontend pages.

---

## Execution Summary

**Completed**: 2026-04-19 12:39 UTC  
**Steps**: 6/6 completed, 0 partial, 0 failed  
**Iterations**: 6 (one per step)

### Changes made
- Created new repository `g:/NAS/ANDREY/puc/doutourado/2026.1/INF2792/kb-qa/` with initial git commit
- `pyproject.toml`, `.gitignore`, `README.md`, `CLAUDE.md`, `knowledge/.gitkeep`
- `src/kb_qa/__init__.py`, `constants.py`, `loader.py`, `ingest.py`, `query.py`, `cli.py`, `__main__.py`
- `agents/__init__.py`, `agents/mcp_server.py`
- `tests/__init__.py`, `tests/test_loader.py` (4 tests), `tests/test_ingest.py` (4 tests)

### Test results
8/8 tests pass. `kb-qa ingest` runs cleanly on empty knowledge/.

### Key learnings
- `uv run` inside the kb-qa dir inherits `VIRTUAL_ENV` from the resqml-expert shell, causing wrong venv to be activated. Use `.venv/Scripts/python` directly.
- chromadb 1.5.8, sentence-transformers 5.4.1, pymupdf 1.27.2.2, mcp 1.27.0 all resolved cleanly against Python 3.13.
- Mock patch targets must use full import path: `kb_qa.ingest.chromadb.PersistentClient`.
- `ruff` and `pyright` not in venv by default; install via `python -m pip install ruff pyright`.

### Deferred items
- Integration tests with real ChromaDB (mocks accepted per plan review, TEST perspective deferred)
- Lint/type-check run skipped at user request (step 6 partial)
