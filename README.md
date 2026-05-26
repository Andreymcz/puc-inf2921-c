# INF2921-Grupo-C

**Course:** INF2921/CIS2114 -- AI Systems Design 2026.1, PUC-Rio  
**Team:** Andrey, Mauro, Julia, Herbert, Natali, Sheila

This repository hosts two related artifacts from the course:

1. **Talk to the City PoC (TRL 3)** -- Talk to the City running entirely locally using Ollama as the LLM backend, with no cloud dependencies (no OpenAI, no Firebase, no GCS).
2. **kb-qa** -- A local RAG knowledge base that ingests `.md` and `.pdf` documents into ChromaDB and exposes `query_knowledge` via MCP.

---

## Talk to the City -- Local PoC (TRL 3)

[Talk to the City](https://talktothe.city/) is an open-source AI-powered platform for synthesizing large-scale qualitative data -- citizen feedback, deliberation transcripts, open survey responses -- into interactive cluster maps. The original system depends on OpenAI, Firebase, Google Cloud Storage, and Cloud Pub/Sub.

This PoC demonstrates that Talk to the City can run fully offline on commodity hardware by substituting every cloud service with local alternatives:

| Cloud dependency | Local substitute |
|-----------------|-----------------|
| OpenAI (embeddings + chat) | Ollama + llama3.2 |
| Firebase Auth | Stubbed TypeScript patch (auto-signs citizen user) |
| Google Cloud Storage | Local filesystem via `LocalFileStorage` patch |
| Cloud Pub/Sub | Redis (already in the original stack) |

The fork used is [`tttc-light-js-ollama`](tttc-poc/tttc-light-js-ollama/), included as a git submodule under `tttc-poc/`.

### Services

| Service | Port | Notes |
|---------|------|-------|
| next-client (Next.js UI) | 3000 | Entry point for the user interface |
| express-server (API) | 8080 | REST API bridging client and pyserver |
| pyserver (FastAPI) | 8000 | Runs analysis pipeline (embedding, clustering, report generation) |
| ollama | 11434 | Local LLM runtime |
| redis | 6379 | Job queue |

### Quick Start

**Prerequisites:** Docker Engine 24+ and the Docker Compose plugin (`docker compose version`). No Python, Node.js, or uv needed on the host.

```bash
# 1. Clone with submodule
git clone --recurse-submodules https://github.com/Andreymcz/puc-inf2921-c.git
cd puc-inf2921-c/tttc-poc

# 2. Build and start all services
docker compose build    # ~5 min on first run
docker compose up -d

# 3. Pull the LLM (first run only -- ~2 GB)
docker exec tttc-poc-ollama-1 ollama pull llama3.2

# 4. Open the UI
# http://localhost:3000
```

Upload `tttc-poc/data/sample-gavealab.csv` (25 qualitative responses on urban challenges in Gavea, Rio) to test the full pipeline end to end.

```bash
# Stop
docker compose down          # preserves the Ollama model volume
docker compose down -v       # also removes the model (frees ~2 GB)
```

See [`tttc-poc/README-poc.md`](tttc-poc/README-poc.md) for the full setup guide, environment variables, and troubleshooting notes.

---

## kb-qa -- Local RAG Knowledge Base

`kb-qa` is a standalone knowledge base for semantic search over a local document corpus. It is used in the course to ground AI-assisted study sessions in course-specific materials (lecture PDFs, papers, research notes) without uploading documents to any cloud service.

### Architecture

```
knowledge/           # Drop .md and .pdf source documents here
  vectorstore/       # ChromaDB PersistentClient (generated, gitignored)
src/kb_qa/           # Python package
  loader.py          # .md and .pdf loading + chunking
  ingest.py          # Embedding pipeline (nomic-ai/nomic-embed-text-v1)
  query.py           # Cosine similarity retrieval + KbQa session class
  constants.py       # Central configuration (model, paths, batch size)
agents/
  mcp_server.py      # FastMCP server -- exposes query_knowledge tool
```

### Quick Start

```bash
uv sync
uv run kb-qa ingest          # ingest all documents in knowledge/
uv run kb-qa status          # show chunk counts and delta
uv run kb-qa ask "question"  # query via CLI
uv run python agents/mcp_server.py  # start MCP server
```

### MCP Integration

Add to `.claude/settings.json` in any Claude Code project:

```json
{
  "mcpServers": {
    "kb-qa": {
      "command": "uv",
      "args": ["run", "python", "agents/mcp_server.py"],
      "cwd": "/absolute/path/to/repo"
    }
  }
}
```

Once configured, Claude automatically calls `query_knowledge` to retrieve relevant chunks from the local knowledge base when answering questions.

---

## Development

```bash
uv run pytest                   # run test suite
uv run ruff check src/          # lint
uv run pyright src/             # type check
```

For the PoC development workflow, see `tttc-poc/Makefile`.
