---
recommended: true
freshness: on-structural-change
diataxis: reference
---

# INF2921 Grupo C — kb-qa

Local RAG knowledge base for course INF2921/CIS2114 (AI Systems Design 2026.1). Ingests `.md` and `.pdf` documents into ChromaDB and exposes a `query_knowledge` MCP tool, allowing Claude and Copilot to retrieve course knowledge during AI assistant sessions.

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | ≥ 3.13 | Runtime |
| uv | latest | Package and environment management |

## Getting Started

### Setup

```bash
git clone https://git.tecgraf.puc-rio.br/arodrigues/inf2921-grupo-c
cd inf2921-grupo-c
uv sync
```

### Ingest documents

```bash
uv run kb-qa ingest knowledge/          # ingest all .md and .pdf files in knowledge/
uv run kb-qa ingest path/to/file.pdf    # ingest a single file
```

### Query

```bash
uv run kb-qa query "What is RAG?"
```

### MCP server (for Claude / Copilot integration)

```bash
uv run python -m agents.mcp_server
```

Add to your MCP client configuration to expose `query_knowledge` during AI assistant sessions.

## Architecture Overview

**Pipeline**: CLI Ingest → Embed (sentence-transformers) → Store (ChromaDB) → MCP Query

| Module | Responsibility |
|--------|---------------|
| `src/kb_qa/cli.py` | Click CLI entry point |
| `src/kb_qa/ingest.py` | Document ingestion pipeline |
| `src/kb_qa/loader.py` | File loaders (.md, .pdf) |
| `src/kb_qa/query.py` | RAG query logic |
| `src/kb_qa/constants.py` | Shared constants |
| `agents/mcp_server.py` | MCP server |

## Running Tests

```bash
uv run pytest
uv run pytest --cov=src/kb_qa
```

## Team

Andrey, Mauro, Julia, Herbert, Natali — INF2921/CIS2114 2026.1 Grupo C
