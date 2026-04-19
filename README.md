# kb-qa

A generic RAG knowledge base that ingests `.md` and `.pdf` files into ChromaDB via sentence-transformers and exposes `query_knowledge` via MCP for SEJA integration.

## Overview

`kb-qa` is a standalone, project-agnostic knowledge base engine. Drop documents into `knowledge/`, run `ingest`, and use `query_knowledge` from any Claude Code project via MCP.

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Place your documents in knowledge/
#    Supported: .md, .pdf

# 3. Ingest documents into the vector store
uv run python -m kb_qa ingest

# 4. Start the MCP server
uv run python agents/mcp_server.py
```

## CLI Commands

```bash
# Ingest all documents in knowledge/ into ChromaDB
uv run python -m kb_qa ingest

# Show vector store status (document count, last ingested)
uv run python -m kb_qa status

# Ask a question via the CLI
uv run python -m kb_qa ask "What is a WellboreTrajectoryRepresentation?"
```

## MCP Integration

Add to your project's `.claude/settings.json`:

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

## Repository Structure

```
knowledge/          # Drop .md and .pdf source documents here
  vectorstore/      # ChromaDB database (generated, gitignored)
src/kb_qa/          # Installable Python package
  ingestion/        # Document loading and chunking
  retrieval/        # ChromaDB query interface
  cli.py            # Click CLI entry points
agents/
  mcp_server.py     # MCP server exposing query_knowledge
tests/              # pytest test suite
```
