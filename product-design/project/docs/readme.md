---
recommended: true
depends_on: [all]
freshness: on-structural-change
diataxis: reference
---

# kb-qa — Local RAG Knowledge Base

> A local RAG knowledge base that ingests `.md` and `.pdf` documents and exposes semantic search via CLI and MCP.

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | ≥ 3.13 | Runtime |
| uv | latest | Package manager |
| Claude Code | any | MCP consumer (optional) |

## Getting Started

```bash
# Install dependencies
uv sync

# Ingest your documents
cp your-docs/*.pdf knowledge/
uv run python -m kb_qa ingest

# Check indexing status
uv run python -m kb_qa status

# Query the knowledge base
uv run python -m kb_qa ask "your question here"
```

## MCP Integration

To use kb-qa with Claude Code, add the following to your project's `.claude/settings.json`:

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

Replace `/absolute/path/to/kb-qa` with the actual absolute path to this repository.

**Prerequisites for MCP**: run `uv run python -m kb_qa ingest` at least once to build the vector store before starting the MCP server.

## Architecture Overview

```
knowledge/          # Source documents (.md, .pdf) — add your files here
  vectorstore/      # ChromaDB database (generated, gitignored)
src/kb_qa/          # Installable Python package
  constants.py      # Model name, paths, batch size
  loader.py         # Document loading (.md, .pdf)
  ingest.py         # Embedding + ChromaDB upsert
  query.py          # Cosine similarity retrieval
  cli.py            # Click CLI (ingest, status, ask)
agents/
  mcp_server.py     # FastMCP server exposing query_knowledge
tests/              # pytest test suite
```

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Type check
uv run pyright src/
```

## Reading Order (new contributors)

1. `product-design/project/constitution.md` — immutable principles
2. `product-design/project/product-design-as-intended.md` — design intent
3. `product-design/conventions.md` — directory and stack variables
4. `src/kb_qa/constants.py` — project-wide constants
5. `src/kb_qa/loader.py` → `ingest.py` → `query.py` — core pipeline
6. `agents/mcp_server.py` — MCP adapter
