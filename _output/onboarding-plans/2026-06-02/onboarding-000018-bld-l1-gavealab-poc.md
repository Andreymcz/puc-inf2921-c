# Onboarding 000018 | BLD L1 | 2026-06-02T00:00:00Z | Builder - GaveaLab PoC

---

## Welcome

Welcome to the INF2921-Grupo-C team. You are joining as a Builder (BLD L1) with a focus on the **GaveaLab PoC** sub-project -- the primary product deliverable of this course project (INF2921/CIS2114, PUC-Rio, 2026.1).

GaveaLab is a citizen-feedback analysis tool: analysts upload CSV files containing citizen comments (relatos), and the application uses a locally running LLM (Ollama) to extract topics, categorize claims, detect divergent opinions between territory groups, and visualize clusters interactively. All inference is local -- no data leaves your machine.

Your role as an L1 Builder is to understand the existing architecture, get the app running locally, and begin contributing through well-scoped tasks under mentor review. The first two weeks will be structured: environment first, codebase orientation second, and then your first PR. This plan gives you the concrete steps to get there.

---

## Layer 0 -- Universal Foundation (Day 1)

### Project Mission and Current Phase

GaveaLab PoC is a Streamlit + Ollama proof-of-concept for citizen-claims analysis. It is inspired by Talk to the City and implements:

- CSV upload and session persistence (SQLite)
- AI-generated topic/subtopic taxonomy via Ollama
- Manual theme categorization
- Claims extraction per subtopic
- Divergent opinion detection (embedding-based cosine distance)
- UMAP 2D cluster visualization (Plotly)

The project is in active PoC development. All major pipeline stages are implemented; the team is now hardening, testing, and extending existing features. Plan-000016 (UMAP visualization) is the most recent completed plan.

**Supporting tool**: `kb-qa` (a local RAG CLI + MCP server in `src/kb_qa/`) runs independently from GaveaLab. You do not need to set it up to work on GaveaLab.

### Team

**Team members**: Andrey, Mauro, Julia, Herbert, Natali, Sheila

Communication norms, meeting cadence, and async channels: _ask your buddy/mentor on Day 1 -- these are not tracked in the repository_.

### Project Glossary

| Term | Definition |
|------|-----------|
| relato | A citizen comment/feedback entry in the CSV dataset |
| session | One analysis run: a named CSV upload stored in SQLite |
| topic_tree | AI-generated JSON taxonomy of topics and subtopics |
| claims_tree | Nested dict of claims extracted per topic/subtopic |
| crux | The core point of disagreement between two territory groups |
| territory | Optional column in the CSV identifying the citizen's region/group |
| Ollama | Local LLM inference server; exposes an OpenAI-compatible REST API |
| UMAP | Dimensionality reduction algorithm used to project claim embeddings into 2D |
| workspace | `GaveaLabWorkspace` -- the single SQLite access point for all persistence |

### AI Tooling Policy

- Use Claude Code (this tool) for code understanding, generation, and review assistance.
- All LLM inference for GaveaLab itself runs through local Ollama -- no cloud LLM calls from the application code.
- AI-generated code must be read and understood before committing. If you cannot explain it in plain language, do not commit it.
- Sanctioned skills: `/explain`, `/research`, `/plan`, `/implement`, `/check`.

---

## Layer 1 -- Role-Specific Context (Week 1)

### Architecture Overview

GaveaLab PoC is a **single-process Streamlit application** with a clear three-layer structure:

```
+---------------------------------------------------------------+
|                  app.py  (Streamlit entry point)             |
|  - Sets page config, creates GaveaLabWorkspace (cached)      |
|  - Sidebar radio: selects which page module to render        |
+---------------------------------------------------------------+
         |                          |
         v                          v
+-------------------+    +------------------------+
|  gavealab_poc/    |    |  gavealab_poc/         |
|  pages/           |    |  pipeline/             |
|                   |    |                        |
|  upload.py        |    |  topics.py             |
|  auto_topics.py   |    |  claims.py             |
|  manual_topics.py |    |  manual_categories.py  |
|  cruxes.py        |    |  cruxes.py             |
|  umap_viz.py      |    |  umap_viz.py           |
+-------------------+    +------------------------+
         |                          |
         |           +--------------+-------------+
         v           v              v             v
+----------------+  +----------+  +-----------+  +----------+
| workspace.py   |  | llm.py   |  |embeddings |  | (SQLite) |
| GaveaLabWork-  |  | OllamaC- |  | .py       |  | gavealab |
| space          |  | lient    |  | e5-large  |  | .db      |
| AnalysisSes-   |  | (OpenAI- |  | (local)   |  |          |
| sion           |  | compat)  |  |           |  |          |
+----------------+  +----------+  +-----------+  +----------+
         |
         v
+-------------------------+
|  Ollama (local process) |
|  qwen2.5:7b (default)   |
|  http://localhost:11434  |
+-------------------------+
```

**Data flow for a full analysis**:

1. User uploads CSV -> `pages/upload.py` calls `workspace.create_session()` -> raw CSV stored in SQLite, `AnalysisSession` created in memory.
2. "Temas automaticos" page -> `pipeline/topics.py::generate_topic_tree()` -> all comments assembled -> `llm.chat()` -> Ollama -> JSON taxonomy parsed -> `session.save_result("topic_tree", ...)` -> SQLite.
3. "Temas automaticos" page -> "Extrair claims" button -> `pipeline/claims.py::extract_claims()` -> per-comment LLM call with taxonomy context -> claims nested dict -> `session.save_result("claims_tree", ...)`.
4. "Opinioes divergentes" page -> `pipeline/cruxes.py::detect_cruxes()` -> all claims embedded via `embeddings.py::embed()` (multilingual-e5-large) -> per-subtopic centroid cosine distance -> divergent subtopics get LLM crux label -> `session.save_result("cruxes", ...)`.
5. "Visualizar clusters" page -> `pipeline/umap_viz.py::build_umap_df()` -> claims flattened -> embeddings -> UMAP 2D projection -> Plotly scatter chart.

### Key Files and Their Roles

| File | Role |
|------|------|
| `gavealab-poc/app.py` | Streamlit entry point; page routing; `GaveaLabWorkspace` creation |
| `gavealab_poc/workspace.py` | `GaveaLabWorkspace` (SQLite persistence); `AnalysisSession` (domain object) |
| `gavealab_poc/llm.py` | `chat()` function; Ollama URL/model from env vars; OpenAI-compat client |
| `gavealab_poc/embeddings.py` | `embed()` with `multilingual-e5-large`; `lru_cache` singleton model |
| `gavealab_poc/pipeline/topics.py` | `generate_topic_tree()`; `_extract_json()` (reused across pipeline) |
| `gavealab_poc/pipeline/claims.py` | `extract_claims()` -- per-comment LLM call with taxonomy |
| `gavealab_poc/pipeline/manual_categories.py` | `categorize_by_themes()` -- user-supplied themes |
| `gavealab_poc/pipeline/cruxes.py` | `detect_cruxes()` -- embedding cosine distance + LLM crux labeling |
| `gavealab_poc/pipeline/umap_viz.py` | `build_umap_df()` -- UMAP projection; returns DataFrame for Plotly |
| `gavealab_poc/pages/*.py` | One file per sidebar page; each exports `render(workspace)` |
| `gavealab-poc/pyproject.toml` | Dependency manifest for the gavealab-poc venv |

### Constitution Constraints You Must Know

These are enforced and violations block commits:

- **T1**: All LLM calls go through `gavealab_poc/llm.py` (`chat()`). Never call httpx or openai directly in pipeline or page modules.
- **T2**: All SQLite access goes through `GaveaLabWorkspace`. Pipeline and page modules call `session.save_result()` -- they never touch the database directly.
- **T3**: Type annotations required on all public functions. Ollama URL and model come from env vars `GAVEALAB_OLLAMA_URL` and `GAVEALAB_OLLAMA_MODEL` only -- never hardcoded.
- **T4**: `gavealab.db` is gitignored. Never commit it.
- **T5**: `GaveaLabWorkspace` is created via `@st.cache_resource` in `app.py` -- exactly one instance per app process.

### Coding Standards

- Python 3.11+ (3.13 recommended).
- `from __future__ import annotations` at the top of every module.
- `snake_case` for functions and variables; `PascalCase` for classes.
- Module-level `log = logging.getLogger(__name__)` -- no `print()` in production code.
- Ruff linting: `uv run ruff check gavealab-poc/` must pass before any commit.
- Pyright type-check: `uv run pyright gavealab-poc/gavealab_poc/` should pass.

### Branch and PR Workflow

- Branch naming: `feat/<short-description>`, `fix/<short-description>`, `chore/<short-description>`.
- Commit messages: imperative mood, concise (e.g., `feat(umap): add territory color filter`).
- Open a PR against `main`; request at least one reviewer.
- First 5 PRs will receive detailed educational feedback -- embrace it.

---

## Layer 2 -- Level-Specific Depth (Weeks 1-4)

### Support Structure

As an L1 Builder, you need a buddy for your first weeks:

| Support | Recommendation |
|---------|---------------|
| Buddy/mentor | Pair with an L2+ team member; daily 15-min check-in for first 2 weeks, then twice weekly for 4 weeks |
| Pair programming | At least 2 hours/week on real tasks for the first month |
| PR review | First 5 PRs reviewed with detailed, educational feedback explaining *why* |

_Ask your team lead to assign a buddy on Day 1._

### Suggested First Task

**Fix or improve the JSON parse robustness in `pipeline/topics.py::_extract_json()`.**

This function is reused across `topics.py`, `claims.py`, and `cruxes.py` (via import). It currently handles two cases (full parse, `{...}` block fallback) but silently returns an empty taxonomy on failure. A well-scoped first task:

1. Add a third fallback: try stripping markdown code fences (` ```json ... ``` `) before parsing.
2. Add a unit test in `tests/test_topics.py` covering the new case.
3. Open a PR.

This task is small, self-contained, tests the PR workflow, and teaches you the pipeline structure.

### Learning Path

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Environment setup + architecture walkthrough + first task scoped | First commit/PR merged |
| 2 | Conventions deep-dive; read all pipeline modules; review one teammate's PR | Second commit + one code review given |
| 3-4 | Independent task: implement a feature or fix from the team backlog | Independent PR completed without architectural guidance |
| 5-8 | Cross-area work: explore pages layer or workspace module; contribute to test coverage | Consistent contributions; decreasing review feedback |

### AI-Assisted Development Guidance (L1 Calibration)

- Use Claude Code to **understand** existing code: "What does `detect_cruxes` do step by step?", "How does `_extract_json` handle malformed LLM output?".
- Use it to **generate code**, but always read and understand what it produces before committing. If you cannot explain a function in plain language, do not commit it.
- Use it to **review your own PRs before submission**: "What could go wrong with this change?", "Am I missing edge cases?".
- Be cautious with AI suggestions about Streamlit session state -- the rerender model is subtle and AI-generated Streamlit code often introduces state bugs.

### Onboarding Milestones

| Milestone | Target | How to verify |
|-----------|--------|--------------|
| GaveaLab app running locally | Day 1 | `streamlit run app.py` shows the UI in browser |
| Ollama running with qwen2.5:7b | Day 1 | `ollama run qwen2.5:7b "Hello"` returns output |
| Architecture mental model | Week 1-2 | Can draw the data-flow diagram from memory |
| First PR merged | Week 1 | PR approved and merged to main |
| Convention fluency | Week 2-4 | PRs pass with minimal style feedback |
| Independent feature delivery | Month 1-2 | End-to-end feature without architectural guidance |

---

## Layer 3 -- Living Knowledge (30-60-90 days)

### Staying Current

- **Briefs file**: `_output/briefs.md` -- execution log of every skill invocation on this project. Read it to understand what changed and why. The most recent entries are the most relevant.
- **Plan history**: `_output/plans/` -- each plan file describes a feature implementation decision. Start with plan-000016 (UMAP) and plan-000013 (cruxes) to understand the most complex pipeline stages.
- **As-coded state**: `product-design/project/product-design-as-coded.md §0` -- the authoritative summary of what is implemented in GaveaLab PoC.

### Quality and Review Standards

- Constitution (`product-design/project/constitution.md`): read it fully in Week 1. Violations are blocking.
- Standards (`product-design/project/standards.md`): covers module responsibilities, naming, logging, error handling.
- Security checklist (`product-design/project/security-checklists.md`): relevant for any new CLI command or pipeline stage.

### Self-Service Learning via Skills

| Task | Command |
|------|---------|
| Understand the codebase architecture | `/explain architecture` |
| Understand a specific behavior | `/explain behavior --area gavealab-poc` |
| Research a new topic | `/research "UMAP parameter tuning"` |
| See what artifacts exist | `/research --inventory` |

---

## How to Install and Run GaveaLab PoC (Windows, PowerShell)

### Prerequisites

- Python 3.11 or 3.13 installed and on PATH
- `uv` package manager installed: `pip install uv` or `winget install astral-sh.uv`
- Git installed
- Ollama installed (see section below)

### Step-by-Step Setup

```powershell
# 1. Clone the repository (if not already done)
git clone https://github.com/YOUR-ORG/inf2921-grupo-c.git
cd inf2921-grupo-c

# 2. Enter the gavealab-poc sub-project directory
cd gavealab-poc

# 3. Create and populate the virtual environment
uv sync

# 4. (Optional) Configure Ollama connection via environment variables
# Defaults: http://localhost:11434/v1 and model qwen2.5:7b
# Only set these if you want to override the defaults:
$env:GAVEALAB_OLLAMA_BASE_URL = "http://localhost:11434/v1"
$env:GAVEALAB_OLLAMA_MODEL = "qwen2.5:7b"

# 5. Start the Streamlit app
uv run streamlit run app.py
```

The app will open at `http://localhost:8501` in your default browser.

### Verifying the Setup

- The sidebar shows: "Upload CSV", "Temas automaticos", "Categorizar por temas", "Opinioes divergentes", "Visualizar clusters".
- Upload a CSV with a `text` or `comment` column to create a session.
- If Ollama is not running, the "Gerar temas com IA" button will fail with a connection error -- that is expected until Ollama is set up (see next section).

### Sample CSV for Testing

Create a file `test_relatos.csv` with this content:

```
id,territory,text
c1,Gavea,O transporte publico precisa de melhorias urgentes nas linhas de onibus
c2,Botafogo,A coleta de lixo na minha rua e irregular ha meses
c3,Gavea,Falta iluminacao nas ruas do bairro tornando as caminhadas inseguras
c4,Ipanema,Os parques estao bem cuidados mas faltam banheiros publicos
c5,Botafogo,O transporte esta horrivel os onibus sempre atrasam
c6,Gavea,A seguranca publica piorou muito nos ultimos meses
c7,Ipanema,Os calcadoes estao em otimo estado porem pouco iluminados a noite
c8,Botafogo,Precisamos de mais areas de lazer para criancas no bairro
```

---

## How to Install and Run Ollama on Windows

Ollama is the local LLM inference server that GaveaLab uses for all AI features. It must be running before you use any pipeline feature (topic generation, claims extraction, crux detection).

### 1. Download and Install Ollama

1. Go to [https://ollama.com/download](https://ollama.com/download) and download the Windows installer (`OllamaSetup.exe`).
2. Run the installer. Ollama installs as a background service and adds `ollama` to your PATH.
3. After installation, Ollama starts automatically and runs in the system tray.

Alternatively, via winget:
```powershell
winget install Ollama.Ollama
```

### 2. Pull the Required Model

GaveaLab defaults to `qwen2.5:7b`. Pull it after installation:

```powershell
# Pull the model (downloads ~4.7 GB on first run)
ollama pull qwen2.5:7b

# Verify the model is available
ollama list
```

Expected output from `ollama list`:
```
NAME            ID              SIZE    MODIFIED
qwen2.5:7b      ...             4.7 GB  a few seconds ago
```

### 3. Verify the Ollama Service is Running

```powershell
# Check that the REST API is reachable
Invoke-WebRequest -Uri "http://localhost:11434" -Method GET | Select-Object StatusCode

# Expected: StatusCode 200

# Or check the version endpoint
Invoke-WebRequest -Uri "http://localhost:11434/api/version" | Select-Object -ExpandProperty Content
```

If Ollama is not running, start it manually:
```powershell
ollama serve
```

Leave that terminal open, or configure Ollama to start with Windows (it does this by default after installation).

### 4. Test the Model Directly

```powershell
# Quick smoke test
ollama run qwen2.5:7b "Responda em JSON: {\"ok\": true}"
```

Expected: Ollama returns a JSON-like response. If this works, GaveaLab pipeline calls will succeed.

### 5. How GaveaLab Connects to Ollama

`gavealab_poc/llm.py` uses the OpenAI-compatible API exposed by Ollama at `http://localhost:11434/v1`. The connection is configured by two environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `GAVEALAB_OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama API base URL |
| `GAVEALAB_OLLAMA_MODEL` | `qwen2.5:7b` | Model name for all LLM calls |

To use a different model (e.g., `llama3.2:3b` for faster responses on low-RAM machines):

```powershell
ollama pull llama3.2:3b
$env:GAVEALAB_OLLAMA_MODEL = "llama3.2:3b"
uv run streamlit run app.py
```

### 6. Embedding Model (multilingual-e5-large)

The cruxes pipeline and UMAP visualization use `intfloat/multilingual-e5-large` via `sentence-transformers` (defined in `gavealab_poc/embeddings.py`). This model is downloaded automatically from HuggingFace on first use (~560 MB). No manual setup required; it runs locally via the `.venv`.

First time you click "Detectar divergencias" or "Gerar visualizacao", expect a 1-3 minute delay for model download. Subsequent calls are fast (model is cached via `lru_cache`).

---

## 30-60-90 Day Plan

### Days 1-7: Foundation

| Activity | Done when |
|----------|-----------|
| Clone repo, run `uv sync` in `gavealab-poc/` | `.venv` created, no errors |
| Install Ollama, pull `qwen2.5:7b`, verify API | `ollama list` shows the model; Invoke-WebRequest returns 200 |
| Run `uv run streamlit run app.py` | App loads in browser at localhost:8501 |
| Upload sample CSV, generate topics (end-to-end test) | topic_tree rendered in "Temas automaticos" |
| Read `app.py`, `workspace.py`, `llm.py`, `embeddings.py` | Can explain each file's role in one sentence |
| Read `product-design/project/constitution.md` | Aware of T1-T5, Q1-Q3, S1-S4 |
| Scope first task with buddy | Task defined, branch created |
| First PR submitted | PR open for review |

**Checkpoint**: buddy reviews environment setup and confirms architecture understanding.

### Days 8-30: Building Fluency

| Activity | Done when |
|----------|-----------|
| First PR merged | Feedback addressed, tests pass |
| Read all pipeline modules (`topics`, `claims`, `manual_categories`, `cruxes`, `umap_viz`) | Can trace the data flow for any page end-to-end |
| Read `product-design/project/standards.md` fully | Coding standards internalized |
| Complete second task independently | PR submitted with no major architectural issues flagged |
| Review at least one teammate PR | Review feedback submitted |
| Run ruff and pyright locally before every PR | Zero linting errors in submitted PRs |

**Checkpoint (Week 4)**: tech lead reviews two merged PRs; confirms convention fluency.

**Success criteria**: PRs pass review with at most minor style comments; can explain any existing module's responsibility without looking at the code.

### Days 31-60: Independent Contribution

| Activity | Done when |
|----------|-----------|
| Complete one independent feature end-to-end | Feature merged without architectural guidance |
| Write unit tests for at least one pipeline module | Tests added in `tests/test_<module>.py` |
| Contribute to one cross-area task (pages layer or workspace) | PR in an area outside your initial focus |
| Use `/explain` or `/research` skills for a non-trivial question | Output artifact created in `_output/` |

**Checkpoint (Day 60)**: buddy sync + tech lead review.

**Success criteria**: independent feature delivery; can onboard the next newcomer to the pipeline modules.

### Days 61-90: Deepening

| Activity | Done when |
|----------|-----------|
| Propose one improvement to an existing module (open an issue or plan) | Proposal documented |
| Give meaningful code review feedback that catches a real issue | Feedback acknowledged by PR author |
| Complete a cross-area contribution outside the pipeline | PR merged in pages, workspace, or app.py layer |
| Understand the embedding + UMAP pipeline well enough to tune parameters | Can explain UMAP `n_neighbors` and `min_dist` trade-offs |

**Checkpoint (Day 90)**: informal 30-min retrospective with buddy and tech lead.

**Success criteria**: recognized as a consistent, independent contributor; reviews trusted by peers.

---

## Recommended Reading List

### Read First (Day 1)

1. `gavealab-poc/app.py` -- entry point and page routing (44 lines)
2. `gavealab-poc/gavealab_poc/workspace.py` -- persistence layer, `AnalysisSession` domain object
3. `gavealab-poc/gavealab_poc/llm.py` -- Ollama client wrapper; env var configuration
4. `product-design/project/constitution.md` -- immutable project principles (T1-T5 are blocking)
5. `gavealab-poc/pyproject.toml` -- dependencies for the gavealab-poc venv

### Read This Week (Week 1)

6. `gavealab-poc/gavealab_poc/embeddings.py` -- sentence-transformers singleton
7. `gavealab-poc/gavealab_poc/pipeline/topics.py` -- topic generation + `_extract_json` (reused everywhere)
8. `gavealab-poc/gavealab_poc/pipeline/claims.py` -- claims extraction
9. `gavealab-poc/gavealab_poc/pipeline/cruxes.py` -- divergence detection algorithm
10. `gavealab-poc/gavealab_poc/pipeline/umap_viz.py` -- UMAP projection
11. `gavealab-poc/gavealab_poc/pages/upload.py` -- CSV upload and session creation UI
12. `product-design/project/standards.md` -- naming, logging, error handling, testing conventions

### Read This Month (Month 1)

13. `gavealab-poc/gavealab_poc/pages/auto_topics.py` -- topics + claims UI
14. `gavealab-poc/gavealab_poc/pages/cruxes.py` -- divergence UI
15. `gavealab-poc/gavealab_poc/pages/umap_viz.py` -- cluster visualization UI
16. `gavealab-poc/gavealab_poc/pages/manual_topics.py` -- manual categorization UI
17. `product-design/project/product-design-as-intended.md` -- full design intent + decisions
18. `product-design/project/product-design-as-coded.md §0` -- current implementation state of GaveaLab PoC
19. `_output/plans/` -- plan files for the features you are working on (start with plan-000013, plan-000016)
20. `_output/briefs.md` -- execution log; understand the project's change history

---

## Appendix: Key Contacts

| Role | Name | Contact | Topics |
|------|------|---------|--------|
| Buddy/Mentor | _TBD_ | | Day-to-day questions, first PR review |
| Tech Lead | _TBD_ | | Architecture decisions, design trade-offs |
| Product Owner / Course Lead | _TBD_ | | Requirements, feature priorities, course alignment |
| QA / Testing | _TBD_ | | Test strategy, pytest conventions |

_Fill in this table with your team lead on Day 1._

---

*Generated by onboarding-generator agent | BLD L1 | gavealab-poc focus | 2026-06-02*
