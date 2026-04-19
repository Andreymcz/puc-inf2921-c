# INF2921 Grupo C — kb-qa

**Course:** INF2921/CIS2114 — AI Systems Design 2026.1 | **Team:** Andrey, Mauro, Julia, Herbert, Natali

Local RAG knowledge base — ingest `.md` and `.pdf` files into ChromaDB via sentence-transformers and expose `query_knowledge` via MCP, injecting course knowledge into Claude and Copilot sessions.

## Project Design References

| File | Contents |
|------|----------|
| `_references/project/conventions.md` | Stack variables, directory paths, build commands |
| `_references/project/constitution.md` | Immutable principles and security invariants |
| `_references/project/product-design-as-intended.md` | Design intent, entity model, decisions |
| `_references/project/product-design-as-coded.md` | Implementation state (agent-maintained) |
| `_references/project/standards.md` | Engineering standards (backend, testing) |
| `_references/project/ux-research-results.md` | Team personas and problem scenarios |

## Stack

- **Python:** 3.13
- **Package manager:** uv
- **Linting:** ruff
- **Type checking:** pyright
- **Testing:** pytest
- **Vector store:** chromadb
- **Embeddings:** sentence-transformers
- **PDF parsing:** pymupdf
- **MCP:** mcp[cli]
- **LLM client:** anthropic

## Common Commands

```bash
# Install dependencies
uv sync

# Ingest all documents in knowledge/ into the vector store
uv run python -m kb_qa ingest

# Show vector store status
uv run python -m kb_qa status

# Ask a question via CLI
uv run python -m kb_qa ask "your question here"

# Start the MCP server
uv run python agents/mcp_server.py

# Run tests
uv run pytest

# Lint
uv run ruff check src/ tests/

# Type check
uv run pyright src/
```

## Repository Structure

```
knowledge/          # Source documents (.md, .pdf) — add your files here
  vectorstore/      # ChromaDB database (generated, gitignored)
src/kb_qa/          # Installable Python package
  ingestion/        # Document loading, chunking, embedding, upsert
  retrieval/        # ChromaDB query interface
  cli.py            # Click CLI (ingest, status, ask)
agents/
  mcp_server.py     # MCP server exposing query_knowledge tool
tests/              # pytest test suite
```

## MCP Integration

The kb-qa MCP server exposes one tool:

| Tool | Description |
|------|-------------|
| `query_knowledge` | Semantic search over the ChromaDB vector store |

To integrate with a Claude Code project, add the following to the project's `.claude/settings.json`:

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

Replace `/absolute/path/to/kb-qa` with the actual absolute path to this repository on the host machine.

**Prerequisites**: Run `uv run python -m kb_qa ingest` at least once to build the vector store before starting the MCP server.

## Key Conventions

- All document ingestion goes through `src/kb_qa/ingestion/` — no ad-hoc file reading elsewhere.
- The vector store lives at `knowledge/vectorstore/` and is gitignored.
- Type annotations required on all public functions.
- No hardcoded paths — use configuration or CLI arguments.
