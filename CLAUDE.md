# INF2921-Grupo-C

Generic RAG knowledge base — ingest .md and .pdf files into ChromaDB and expose `query_knowledge` via MCP.

**Course:** INF2921/CIS2114 — AI Systems Design 2026.1 | **Team:** Andrey, Mauro, Julia, Herbert, Natali

## Stack

- **Python:** 3.13
- **Package manager:** uv
- **Testing:** pytest
- **Vector store:** ChromaDB
- **Embeddings:** sentence-transformers
- **PDF parsing:** pymupdf
- **MCP:** mcp[cli]
- **LLM client:** anthropic SDK
- **CLI:** click

## Build & Run

```bash
# Install dependencies
uv sync

# Ingest all documents in knowledge/ into the vector store
uv run kb-qa ingest

# Show vector store status
uv run kb-qa status

# Ask a question via CLI
uv run kb-qa ask "your question here"

# Start the MCP server
uv run python agents/mcp_server.py

# Run tests
uv run pytest

# Lint
uv run ruff check src/ tests/

# Type check
uv run pyright src/
```

## Project Shape

CLI + MCP server tool — not a web application. The package exposes a `kb-qa` CLI (click) for ingesting documents and querying the vector store, and an MCP server (`agents/mcp_server.py`) that exposes `query_knowledge` as a tool for Claude and Copilot sessions.

For directory layout, stack variables, and engineering conventions, see `product-design/conventions.md`.

## Key Conventions

- All document ingestion goes through `src/kb_qa/ingestion/` — no ad-hoc file reading elsewhere.
- The vector store lives at `knowledge/vectorstore/` and is gitignored.
- Type annotations required on all public functions.
- No hardcoded paths — use configuration or CLI arguments.

## Skills & Design References

This project uses Claude Code skills (`.claude/skills/`). Skills are invoked via `/skill-name`. Main lifecycle: `/research` > `/plan` > `/implement` > `/check` > `/document`.

@.claude/rules/
@product-design/conventions.md

## Project Design

@product-design/project/product-design-as-intended.md
@product-design/project/ux-research-results.md
@product-design/project/standards.md
@product-design/project/design-standards.md
@product-design/project/security-checklists.md
@product-design/project/constitution.md
