# INF2921-Grupo-C — GaveaLab

Local citizen feedback analysis tool for INF2921/CIS2114 (AI Systems Design, PUC-Rio 2026.1).  
**Team:** Andrey, Mauro, Julia, Herbert, Natali, Sheila

---

## What is GaveaLab?

GaveaLab lets researchers upload a CSV of citizen relatos (open-ended survey responses or public consultation comments) and analyze them through a local LLM pipeline — topic extraction, claim categorization, divergence detection, and UMAP cluster visualization — without sending data to any cloud service.

Inspired by [Talk to the City](https://github.com/AIObjectives/talk-to-the-city-reports).

---

## Quick Start

### Prerequisites

- **Python 3.11+**: `python --version`
- **uv**: `uv --version` — if missing: `winget install astral-sh.uv`
- **Ollama**: [ollama.com/download/windows](https://ollama.com/download/windows) or `winget install Ollama.Ollama`

### 1. Install dependencies

```powershell
cd gavealab-poc
uv sync
```

### 2. Pull the LLM model and start Ollama

```powershell
ollama pull qwen2.5:7b
ollama serve          # skip if Ollama is already running in the system tray
```

### 3. Launch the app

```powershell
# From the repository root:
uv run streamlit run gavealab-poc/app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## App Pages

| Page | What it does |
|------|-------------|
| **Upload CSV** | Upload a citizen-relatos CSV (`text` or `comment` column required). Creates a named session persisted in `gavealab.db`. |
| **Temas automáticos** | LLM-powered topic hierarchy extraction from the uploaded relatos. |
| **Categorizar por temas** | Manually assign relatos to topics; embeddings suggest matches. |
| **Opiniões divergentes** | Detects cruxes — points of genuine disagreement between citizen claims. |
| **Visualizar clusters** | UMAP 2D scatter plot of claim embeddings (Plotly). Hover to read the original comment. |

Workflow: upload → auto-topics → claims → cruxes → visualization. All results persist in `gavealab.db` — reload a session without reprocessing.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GAVEALAB_OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama OpenAI-compatible endpoint |
| `GAVEALAB_OLLAMA_MODEL` | `qwen2.5:7b` | LLM model name |

```powershell
$env:GAVEALAB_OLLAMA_MODEL = "llama3.2:3b"   # lighter alternative for CPU-only machines
```

---

## Repository Structure

```
gavealab-poc/              # Primary product (Streamlit app)
  app.py                   # Entry point — page router
  gavealab.db              # SQLite database (auto-created, gitignored)
  pyproject.toml
  gavealab_poc/
    llm.py                 # OllamaClient — all LLM calls go here
    workspace.py           # GaveaLabWorkspace + AnalysisSession (SQLite)
    embeddings.py          # embed() — multilingual-e5-large
    pipeline/              # Stateless LLM pipeline steps
      topics.py            # Auto topic extraction
      claims.py            # Claim extraction
      cruxes.py            # Divergence detection
      manual_categories.py # Manual theme categorization
      umap_viz.py          # UMAP projection
    pages/                 # Streamlit page modules
      upload.py
      auto_topics.py
      manual_topics.py
      cruxes.py
      umap_viz.py

src/kb_qa/                 # Supporting RAG tool (kb-qa) — maintenance only
agents/
  mcp_server.py            # MCP server exposing query_knowledge
knowledge/                 # Drop .md/.pdf documents here for kb-qa
  vectorstore/             # ChromaDB index (generated, gitignored)
```

---

## kb-qa (Supporting Tool)

kb-qa is a supporting RAG tool for querying course documents (lecture notes, papers) from Claude Code sessions via MCP. It is not the primary course deliverable.

```bash
cd src
uv sync

uv run kb-qa ingest          # Index documents in knowledge/
uv run kb-qa status          # Show vector store state
uv run kb-qa ask "question"  # Query via CLI

uv run python agents/mcp_server.py   # Start the MCP server
```

**MCP integration** — add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "kb-qa": {
      "command": "uv",
      "args": ["run", "python", "agents/mcp_server.py"],
      "cwd": "/absolute/path/to/inf2921-grupo-c"
    }
  }
}
```

---

## Tests & Quality

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check src/ gavealab-poc/

# Type check
uv run pyright src/
```
