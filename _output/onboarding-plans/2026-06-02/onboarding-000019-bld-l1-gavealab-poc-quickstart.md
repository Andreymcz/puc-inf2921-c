# Onboarding 000019 | BLD L1 | gavealab-poc Quickstart | 2026-06-02 00:00 UTC

---

## Section 1: Tech Stack

This document covers the `gavealab-poc` sub-project: a Streamlit web application for citizen feedback analysis (topic extraction, claim categorization, divergence detection, and UMAP cluster visualization). It is the primary product of INF2921-Grupo-C and lives under `gavealab-poc/`.

### Runtime and Package Management

| Technology | What it is | Why it is used here |
|---|---|---|
| **Python 3.11+** | General-purpose programming language | Project baseline; `gavealab-poc/pyproject.toml` sets `requires-python = ">=3.11"` |
| **uv** | Fast Python package manager and virtual-environment tool | Manages dependencies via `pyproject.toml` + `uv.lock`; replaces pip/venv for consistent, reproducible installs across the team |

### UI Framework

| Technology | What it is | Why it is used here |
|---|---|---|
| **Streamlit >= 1.35** | Python-native web UI framework that turns scripts into interactive apps | Provides the entire browser-based UI with zero frontend code -- sidebar navigation, file upload widget, charts, and result tables are all written in Python |

### Data Handling

| Technology | What it is | Why it is used here |
|---|---|---|
| **pandas >= 2.2** | DataFrame library for tabular data manipulation | Loads and normalizes the citizen-relatos CSV files; the `_parse_csv` function in `workspace.py` canonicalizes column names and filters short entries |
| **SQLite (stdlib)** | Embedded relational database, accessed via Python's built-in `sqlite3` module | `GaveaLabWorkspace` in `gavealab_poc/workspace.py` persists sessions and analysis results to `gavealab.db` so work survives browser refreshes |
| **numpy >= 1.26** | N-dimensional array library | Used by the embeddings layer to store and manipulate embedding vectors before passing them to UMAP |

### Embeddings

| Technology | What it is | Why it is used here |
|---|---|---|
| **sentence-transformers >= 3.0** | Library for computing dense sentence/paragraph embeddings using pre-trained transformer models | Drives all semantic similarity computations -- topic clustering and claim categorization both depend on embedding citizen relatos into vector space |
| **intfloat/multilingual-e5-large** | A multilingual embedding model (~560MB, supports 100+ languages including pt-BR) | Chosen for strong multilingual quality so that Portuguese citizen comments embed accurately alongside English metadata; model name is hardcoded in `gavealab_poc/embeddings.py` as `EMBED_MODEL` |

### Local LLM Inference

| Technology | What it is | Why it is used here |
|---|---|---|
| **Ollama** | A local LLM runtime that serves open-source models (Llama, Qwen, Mistral, etc.) via an OpenAI-compatible REST API on `http://localhost:11434` | Provides LLM-powered topic extraction, claim analysis, and divergence detection without sending citizen data to any cloud provider -- aligns with the project's privacy-first principle |
| **openai >= 1.30 (SDK)** | Python client for the OpenAI API | Used as the HTTP client to talk to Ollama's OpenAI-compatible endpoint (`/v1/chat/completions`); no actual OpenAI account or key is needed |
| **qwen2.5:7b** (default model) | A 7-billion-parameter instruction-tuned LLM from Alibaba, quantized for local CPU/GPU inference | Default configured in `gavealab_poc/llm.py`; override via `GAVEALAB_OLLAMA_MODEL` env var. The `extra_body={"think": False}` flag disables chain-of-thought mode for faster responses |

### Visualization

| Technology | What it is | Why it is used here |
|---|---|---|
| **umap-learn >= 0.5** | Implements UMAP (Uniform Manifold Approximation and Projection), a dimensionality reduction algorithm | Reduces the high-dimensional embedding vectors (1024-dim for multilingual-e5-large) to 2D coordinates so claim clusters can be plotted on a scatter chart |
| **plotly >= 5.0** | Interactive charting library with browser-native zoom/pan/hover | Renders the 2D UMAP scatter plot in the "Visualizar clusters" page; hover tooltips display the original citizen comment text |

### Source Layout

```
gavealab-poc/
  app.py                          # Streamlit entry point -- page router
  gavealab.db                     # SQLite database (auto-created on first run)
  pyproject.toml                  # Project dependencies and metadata
  gavealab_poc/
    embeddings.py                 # embed() -- wraps multilingual-e5-large
    llm.py                        # chat() -- wraps Ollama via openai SDK
    workspace.py                  # GaveaLabWorkspace + AnalysisSession (SQLite persistence)
    pages/
      upload.py                   # Page: Upload CSV
      auto_topics.py              # Page: Temas automaticos (LLM topic extraction)
      manual_topics.py            # Page: Categorizar por temas
      cruxes.py                   # Page: Opinioes divergentes (divergence detection)
      umap_viz.py                 # Page: Visualizar clusters (UMAP + Plotly)
    pipeline/
      claims.py                   # Claim extraction pipeline
      cruxes.py                   # Divergence detection pipeline
      manual_categories.py        # Manual categorization pipeline
      topics.py                   # Automatic topic extraction pipeline
      umap_viz.py                 # UMAP dimensionality reduction pipeline
```

---

## Section 2: How to Run the System

### Step 1 -- Prerequisites

Before you start, verify you have the following installed:

- **Python 3.11 or later**: `python --version`
- **uv**: `uv --version` -- if missing, install with:
  ```powershell
  winget install astral-sh.uv
  ```
  or download the installer from https://docs.astral.sh/uv/getting-started/installation/
- **Git**: `git --version`

### Step 2 -- Clone and Install Dependencies

```powershell
git clone https://github.com/<your-org>/inf2921-grupo-c.git
cd inf2921-grupo-c

# Install all dependencies for gavealab-poc into an isolated virtual environment
cd gavealab-poc
uv sync
```

`uv sync` reads `pyproject.toml` and `uv.lock` and installs exact pinned versions. The first run also downloads the `intfloat/multilingual-e5-large` model (~560MB) from Hugging Face the first time you launch the app, so expect a delay on first startup.

### Step 3 -- Install and Start Ollama

Ollama provides the local LLM inference backend. The app will fail to perform any LLM-powered analysis without it.

**3a. Install Ollama**

Option A -- winget (recommended):
```powershell
winget install Ollama.Ollama
```

Option B -- direct installer:
Download from https://ollama.com/download/windows and run the `.exe` installer.

**3b. Start the Ollama server**

After installation, Ollama may start automatically as a system tray application. If not, start it explicitly:
```powershell
ollama serve
```

Leave this terminal open, or verify it is running in the tray.

**3c. Pull the default model**

```powershell
ollama pull qwen2.5:7b
```

This downloads the model (~4.7GB). Wait for the download to complete before running the app.

**3d. Verify Ollama is responding**

```powershell
Invoke-WebRequest -Uri http://localhost:11434/api/tags -UseBasicParsing | Select-Object -ExpandProperty Content
```

Expected: a JSON response listing available models including `qwen2.5:7b`.

### Step 4 -- Set Environment Variables

The app reads two optional environment variables. If not set, defaults are used (`http://localhost:11434/v1` and `qwen2.5:7b`).

```powershell
# Set for the current PowerShell session
$env:GAVEALAB_OLLAMA_BASE_URL = "http://localhost:11434/v1"
$env:GAVEALAB_OLLAMA_MODEL    = "qwen2.5:7b"
```

To use a different Ollama model (for example, a lighter `llama3.2:3b` for faster responses on CPU-only machines):
```powershell
ollama pull llama3.2:3b
$env:GAVEALAB_OLLAMA_MODEL = "llama3.2:3b"
```

### Step 5 -- Launch the Streamlit App

Run the following from the repository root:
```powershell
uv run streamlit run gavealab-poc/app.py
```

Or, if you are already inside `gavealab-poc/`:
```powershell
uv run streamlit run app.py
```

Streamlit will print something like:
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open http://localhost:8501 in your browser.

### Step 6 -- What to Expect in the Browser

The app opens to a sidebar with five pages:

| Page | What it does |
|---|---|
| **Upload CSV** | Upload a citizen-relatos CSV file. Required column: `text` or `comment`. Optional: `id`, `territory`. Creates a named analysis session persisted in `gavealab.db`. |
| **Temas automaticos** | Calls Ollama to extract a topic hierarchy from the uploaded relatos using LLM-based analysis. Results are saved to the session. |
| **Categorizar por temas** | Manually assign relatos to topics; uses embeddings to suggest category matches. |
| **Opinioes divergentes** | Detects claims where citizens hold strongly opposing views (divergence/crux detection). |
| **Visualizar clusters** | Runs UMAP on the claim embeddings and displays an interactive 2D scatter plot with Plotly. Hover over a point to read the original relato text. |

The workflow is sequential: upload a CSV first, then run automatic topics, then explore clusters or divergences. All results are persisted in `gavealab.db` -- you can reload a session without reprocessing.

---

*Generated by onboarding-generator | Onboarding 000019 | 2026-06-02 00:00 UTC*
