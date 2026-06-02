# Onboarding 000017 | BLD L1 | 2026-06-02T00:00:00Z | Builder -- L1 Contributor

---

## Welcome

Welcome to INF2921-Grupo-C. You are joining as a Builder (BLD) at the L1 Contributor level, meaning your focus is writing, running, and iterating on code while you build familiarity with the project's conventions, architecture, and team workflow.

This project has two deliverables that live in the same repository:

- **GaveaLab** (`gavealab-poc/`) -- the primary product: a Streamlit + Ollama citizen-claims analysis tool. This is the active delivery front.
- **kb-qa** (`src/kb_qa/`) -- a supporting local RAG CLI and MCP server built on ChromaDB and sentence-transformers.

Your first weeks will be structured around getting the environment running, understanding the codebase structure, making a first small contribution, and building a mental model of how the two products relate. You will have a buddy or mentor to support you. Expect detailed feedback on your first pull requests -- it is meant to be educational, not critical.

---

## Layer 0 -- Universal Foundation (Day 1)

### Project Mission and Current Phase

INF2921-Grupo-C is a course project for INF2921/CIS2114 AI Systems Design 2026.1 at PUC-Rio. Team: Andrey, Mauro, Julia, Herbert, Natali e Sheila.

**Primary product -- GaveaLab**: A citizen feedback analysis tool inspired by Talk to the City. It reads CSV datasets of citizen `relatos` (comments), runs LLM-powered topic extraction, claims analysis, divergence detection, and UMAP cluster visualization. Runs as a local Streamlit app with Ollama as the LLM backend.

**Supporting tool -- kb-qa**: A privacy-first local RAG knowledge base. Ingests `.md` and `.pdf` documents into a ChromaDB vector store and exposes semantic search via a CLI (`kb-qa ask`) and an MCP tool (`query_knowledge`) for use in Claude sessions.

Current phase: active feature development on GaveaLab. The kb-qa tool is in a stable baseline state with planned v0.2 improvements (session-reuse CLI, similarity score exposure).

### Team Structure and Communication Norms

_The team should fill in the following details:_

| Topic | Details |
|-------|---------|
| Stand-up / sync cadence | _TBD_ |
| Primary communication channel | _TBD_ |
| PR review turnaround expectation | _TBD_ |
| Where to ask questions | _TBD_ |
| Sprint or milestone cadence | _TBD_ |

### Environment Setup

**Prerequisites**: Python 3.13, `uv` package manager, Ollama (for GaveaLab LLM calls), Git.

**Step 1: Clone and install dependencies**

```bash
# Clone the repository
git clone <repo-url>
cd inf2921-grupo-c

# Install all dependencies (including dev) for kb-qa
uv sync

# Install GaveaLab dependencies (separate pyproject.toml)
cd gavealab-poc
uv sync
cd ..
```

**Step 2: Verify kb-qa**

```bash
# Run all tests -- should pass with no errors
uv run pytest

# Lint check
uv run ruff check src/

# Type check
uv run pyright src/
```

**Step 3: Verify GaveaLab**

```bash
cd gavealab-poc

# Run the Streamlit app (requires Ollama running locally)
uv run streamlit run gavealab_poc/app.py
```

**Step 4: Environment variables**

GaveaLab reads two env vars for Ollama configuration. Set them in your shell or a local `.env` file (never commit `.env`):

```
GAVEALAB_OLLAMA_URL=http://localhost:11434
GAVEALAB_OLLAMA_MODEL=<model-name>
```

**Step 5: Ingest sample documents into kb-qa (optional)**

```bash
# Place .md or .pdf files in knowledge/
# Then ingest:
uv run kb-qa ingest

# Check status
uv run kb-qa status
```

Target: clone to passing tests under 5 minutes (first run will download the `nomic-ai/nomic-embed-text-v1` embedding model, ~274 MB -- this is normal and happens only once).

### Project Glossary

| Term | Definition |
|------|-----------|
| **GaveaLab** | The primary Streamlit-based citizen feedback analysis product in `gavealab-poc/` |
| **kb-qa** | The local RAG CLI and MCP supporting tool in `src/kb_qa/` |
| **relato** | A citizen comment/feedback entry; the atomic input unit in GaveaLab CSV datasets |
| **KnowledgeDocument** | A `.md` or `.pdf` file placed in `knowledge/` for ingestion into kb-qa |
| **Chunk** | A text segment extracted from a KnowledgeDocument; the atomic unit stored in ChromaDB |
| **VectorStore** | ChromaDB `PersistentClient` collection named `kb-qa-docs` at `knowledge/vectorstore/` |
| **MCP tool** | `query_knowledge` -- the FastMCP tool exposed by `agents/mcp_server.py` |
| **GaveaLabWorkspace** | The SQLite persistence layer for GaveaLab sessions and results |
| **AnalysisSession** | A GaveaLab domain object representing one analysis run over a CSV dataset |
| **topic tree** | Hierarchical topic/subtopic taxonomy extracted by LLM from citizen comments |
| **claim** | An atomic assertion extracted per-comment, linked to a topic/subtopic |
| **crux** | A detected point of divergence between territory groups (cosine distance > 0.25) |
| **UMAP** | Dimensionality reduction algorithm used for cluster visualization of claim embeddings |
| **OllamaClient** | The centralized LLM wrapper in `gavealab_poc/llm.py` -- all LLM calls go through here |
| **content-addressable ID** | MD5 of `source + text[:200]` used to deduplicate Chunks during ingestion |
| **nomic-embed-text-v1** | The sentence-transformers embedding model used by kb-qa for multilingual semantic search |
| **multilingual-e5-large** | The sentence-transformers model used by GaveaLab's `embeddings.py` for claim embeddings |
| **plan** | A numbered artifact (`plan-NNNNNN`) describing an implementation step; stored in `_output/plans/` |

Also see `product-design/project/product-design-as-intended.md §3` for domain-specific concept definitions.

### AI Tooling Policy and Sanctioned Tools

- **Claude Code** (claude-sonnet-4-6) is the primary AI assistant and is used via the `/onboard`, `/implement`, `/explain`, `/research`, `/plan`, `/check`, and `/document` skills in `.claude/skills/`.
- **Ollama** (local) is the LLM backend for GaveaLab analysis pipelines.
- AI-generated code must be read and understood before committing. Never treat AI output as a black box.
- Constitution invariants (T1-T4, Q1-Q3, S1-S3) are enforced -- AI suggestions that violate them must be rejected or adjusted.
- If AI generates a hardcoded path, model name, or API key: reject it and use the constants/env-var pattern instead.

---

## Layer 1 -- Role-Specific Context (Week 1)

### Architecture Overview

The repository contains two independent Python packages:

```
inf2921-grupo-c/
|-- gavealab-poc/              # Primary product -- Streamlit app
|   |-- gavealab_poc/
|   |   |-- app.py             # Sidebar + page routing
|   |   |-- llm.py             # OllamaClient -- ALL LLM calls go here (T1)
|   |   |-- embeddings.py      # SentenceTransformer singleton (multilingual-e5-large)
|   |   |-- workspace.py       # GaveaLabWorkspace -- ALL SQLite access here (T2)
|   |   |-- pipeline/
|   |   |   |-- topics.py      # LLM-powered topic tree generation
|   |   |   |-- claims.py      # Per-comment claim extraction
|   |   |   |-- manual_categories.py  # User-defined theme categorization
|   |   |   |-- cruxes.py      # Divergence detection (embeddings + LLM labels)
|   |   |   `-- umap_viz.py    # UMAP 2D embedding and Plotly chart
|   |   `-- pages/
|   |       |-- upload.py      # CSV upload + session management
|   |       |-- auto_topics.py # Topic tree + claim extraction UI
|   |       |-- manual_topics.py  # Manual theme categorization UI
|   |       |-- cruxes.py      # Divergence detection UI
|   |       `-- umap_viz.py    # UMAP cluster visualization UI
|   `-- pyproject.toml         # Separate uv venv for GaveaLab
|
|-- src/kb_qa/                 # Supporting tool -- kb-qa CLI and MCP
|   |-- cli.py                 # Click commands: ingest, status, ask
|   |-- constants.py           # All constants (model name, paths, collection name)
|   |-- loader.py              # Document loading (.md + .pdf) via pymupdf
|   |-- ingest.py              # Embedding pipeline + ChromaDB upsert
|   |-- query.py               # Cosine similarity retrieval; KbQa session class
|   `-- __init__.py / __main__.py
|-- agents/
|   `-- mcp_server.py          # FastMCP server exposing query_knowledge
|-- tests/                     # pytest tests for kb-qa
|-- knowledge/                 # User-managed .md/.pdf source documents
|   `-- vectorstore/           # ChromaDB database -- gitignored (S2)
`-- product-design/            # Design intent, as-coded state, conventions
```

**Data flow for GaveaLab (happy path)**:
1. User uploads CSV via `pages/upload.py` -> `workspace.create_session()` stores in SQLite
2. User generates topics via `pages/auto_topics.py` -> `pipeline/topics.py` -> `llm.chat()` -> persisted via `session.save_result()`
3. User extracts claims -> `pipeline/claims.py` -> same pattern
4. User runs UMAP viz -> `pipeline/umap_viz.py` -> `embeddings.embed()` -> `umap.UMAP` -> Plotly scatter

**Data flow for kb-qa**:
1. `kb-qa ingest` -> `loader.load_all()` -> `ingest.ingest()` -> `SentenceTransformer.encode()` -> ChromaDB upsert
2. `kb-qa ask` or MCP `query_knowledge` -> `query.retrieve()` -> `SentenceTransformer.encode(question)` -> ChromaDB cosine query

### Coding Conventions

Key rules to internalize on Day 1:

| Convention | Rule | Where enforced |
|-----------|------|---------------|
| All LLM calls | Must go through `gavealab_poc/llm.py` (OllamaClient) -- never direct httpx | Constitution T1 |
| All SQLite access | Must go through `GaveaLabWorkspace` -- never direct DB access in pipeline/page modules | Constitution T2 |
| Type annotations | Required on all public functions | Constitution T3 / pyright |
| No hardcoded paths or model names | Use `constants.py` (kb-qa) or env vars (GaveaLab) | Constitution T3 / T5 |
| `gavealab.db` and `knowledge/vectorstore/` | Never committed to git | Constitution T4 / S2 |
| Logging | Use `logging` module -- no `print()` in operational code | `product-design/project/standards.md §5` |
| Naming | `snake_case` for modules/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants | `product-design/project/standards.md §6` |
| Tests | `tmp_path` fixture for all filesystem operations in tests -- never touch real `knowledge/vectorstore/` | `product-design/project/standards.md § Testing` |

Read `product-design/project/standards.md` in full during Week 1.

### Branching and PR Workflow

_The team should document specifics; defaults below:_

- Branch naming: `<type>/<short-description>` (e.g., `fix/upload-validation`, `feat/score-visibility`)
- Commit messages: imperative mood, present tense (e.g., "add similarity score to ask output")
- PRs: request review from at least one team member before merge
- First 5 PRs will receive detailed, educational review feedback -- expect comments explaining _why_, not just _what_

### CI/CD Pipeline

_The team should document CI setup. Current state:_

- Linting: `uv run ruff check src/`
- Type checking: `uv run pyright src/`
- Tests: `uv run pytest`
- Deployment: local / personal NAS -- no automated deployment pipeline documented yet

Run all three locally before pushing any branch.

### AI-Assisted Development Workflow

1. Use AI to **explore** the codebase: "What does `_doc_id()` do?", "How does the cruxes pipeline work?"
2. Use AI to **accelerate context**: "Explain the data flow for topic extraction", "What are the naming conventions for this project?"
3. Use AI to **generate and review code** -- but always run `ruff`, `pyright`, and `pytest` on the result
4. Read every line of AI-generated code before committing -- if you cannot explain it in plain language, do not commit it
5. Check AI suggestions against constitution invariants T1-T5 -- reject any suggestion that adds direct DB calls, hardcoded model names, or inline file paths

---

## Layer 2 -- Level-Specific Depth (Weeks 1-4)

### Support Structure

You are an L1 Contributor. The right support depends on your experience level:

| Support type | Newcomer (0-2 yrs) | Practitioner (2-5 yrs) |
|-------------|--------------------|-----------------------|
| Buddy/mentor | Pair with an L2+ team member; daily 15-min check-ins for 2 weeks, then twice weekly | Weekly 30-min sync with an L2+ for first month |
| Pair programming | Minimum 2 hrs/week for first month on real tasks | 1-hr architecture walkthrough with a senior on key design decisions |
| PR review style | First 5 PRs get detailed educational feedback explaining the _why_ | 1-hr domain session with a team member on user goals and product direction |

### Concrete First Task Suggestion

The project's `product-design/project/product-design-as-intended.md §0` lists planned v0.2 improvements for kb-qa:

**Recommended first task**: Add an explicit "Downloading embedding model..." message before the first `SentenceTransformer()` call in `src/kb_qa/ingest.py` (or `src/kb_qa/query.py`), or check whether the model is cached and inform the user. This addresses the observed friction in `ux-research-results.md § JM-E-001`.

Why this is a good first task:
- It is well-scoped (one function, one file)
- It does not require changing the architecture
- It gives you hands-on experience with the ingestion pipeline
- You will learn how `SentenceTransformer` caching works
- It has a clear acceptance criterion: a message appears on first run and is suppressed on subsequent runs

Alternative first task: expose similarity scores in the `ask` command output (planned v0.2 feature in `§0`) -- slightly larger scope but still well-contained in `src/kb_qa/cli.py` and `src/kb_qa/query.py`.

### Learning Path

| Week | Focus | Deliverable |
|------|-------|------------|
| 1 | Environment setup + first commit | Tests pass locally; first PR submitted (model-download message or score visibility) |
| 2 | Read `standards.md` + `product-design-as-coded.md` in full; trace GaveaLab upload-to-topics flow in code | Second commit + one code review given |
| 3-4 | Independent task: pick a well-scoped item from the backlog or `product-design-as-intended.md §0` planned changes | Independent PR merged with minimal style feedback |
| 5-8 | Cross-area exploration: contribute to either GaveaLab pipeline or kb-qa; participate in one architecture discussion | Consistent contributions; begin reviewing others' PRs substantively |

### Onboarding Milestones

| Milestone | Target | How to verify |
|-----------|--------|--------------|
| Environment running | Day 1 | `uv run pytest` passes locally |
| First commit merged | Week 1 | PR approved and merged by buddy/mentor |
| Architecture mental model | Week 1-2 | Can sketch the GaveaLab pipeline (upload -> topics -> claims -> cruxes -> UMAP) from memory |
| Convention fluency | Week 2-4 | PRs pass review without type annotation, naming, or import boundary comments |
| Independent feature delivery | Month 1-2 | End-to-end feature without architectural guidance |
| Meaningful code reviews | Month 2-3 | Review comments catch real issues (not just style) |

### Material Format Guidance

- **Newcomers**: start with the step-by-step setup above; read one file at a time from the reading list; ask your buddy before reading architecture docs
- **Practitioners**: read `standards.md` and `product-design-as-coded.md §0` on Day 1; trace the data flow code yourself; use the reading list as a checklist

### AI-Assisted Development -- L1 Reminders

- Red flag: if you cannot explain a code block in one sentence, do not commit it
- Use Claude to understand existing code before writing new code
- When AI suggests a pattern, ask yourself: does this match `standards.md`? Does it violate any constitution principle?
- Run `uv run ruff check src/` and `uv run pyright src/` after every AI-assisted edit

---

## Layer 3 -- Living Knowledge (30-60-90 Days)

### Decision Context

As you work, you will encounter design decisions. Read `product-design/project/product-design-as-intended.md §§ Decisions` for the rationale behind key choices (ChromaDB, MCP via FastMCP, nomic-embed-text-v1). These explain _why_ the architecture is the way it is -- read them before proposing changes.

### Review Perspectives Framework

Quality standards are encoded in `.claude/references/general/review-perspectives/`. When you are ready to review PRs yourself (Month 2-3), familiarize yourself with the `dx.md` perspective (developer experience standards). Your buddy can guide you to the right perspectives for your area.

### Skill System for Self-Service Learning

The project uses Claude Code skills for structured analysis and generation. As you become comfortable:

- `/explain behavior <topic>` -- get an explanation of how a specific feature or pipeline works
- `/explain architecture` -- generate an architecture overview if one does not exist
- `/explain data-model` -- generate a data model explanation
- `/research <topic>` -- run a structured research session on a technical question
- `/research --inventory` -- see all available research logs

To invoke: type `/skill-name` in your Claude Code session. Skills handle the full lifecycle including reading project context.

### Plan History

All implementation plans are in `_output/plans/`. Reading recent plans (e.g., `plan-000016` for the UMAP cluster visualization) gives you a window into _how_ features were designed and implemented, including trade-offs considered. This is the best way to understand the "why" behind recent code changes.

---

## 30-60-90 Day Plan

### Days 1-30: Foundation

| Week | Activity | Success Criteria |
|------|----------|-----------------|
| Day 1 | Environment setup: clone, `uv sync`, `uv run pytest` passes, GaveaLab Streamlit app launches | All tests green; app renders in browser |
| Day 1 | Read: `CLAUDE.md`, `product-design/conventions.md`, `product-design/project/constitution.md` | Can state the 5 technical principles from memory |
| Week 1 | Read `product-design/project/standards.md` in full | Aware of module responsibilities and naming rules |
| Week 1 | Trace the GaveaLab upload flow in code: `pages/upload.py` -> `workspace.py` | Can explain the flow verbally |
| Week 1 | Submit first PR (model-download message or score visibility) | PR approved by buddy |
| Week 2 | Read `product-design/project/product-design-as-coded.md` fully | Can describe both products and their relationship |
| Week 2 | Trace GaveaLab topics -> claims -> cruxes pipeline in code | Can explain each pipeline step |
| Week 3-4 | Independent task from backlog | PR merged with minimal feedback |

**Checkpoint**: End of Month 1 -- 30-min sync with buddy/mentor. Can the new contributor explain the architecture, name the key modules, and describe their first two PRs?

### Days 31-60: Growing Independence

| Activity | Success Criteria |
|----------|-----------------|
| Second independent feature or meaningful bug fix | PR merged without architectural guidance |
| Give substantive code review on one PR | Review identifies a real issue or improvement |
| Read `product-design/project/product-design-as-intended.md §§ 0, 13, 14` | Understands planned improvements and user stories |
| Explore `agents/mcp_server.py` and run the MCP server locally | Understands the MCP tool boundary |
| Begin cross-area exploration (if started on kb-qa: look at GaveaLab; if GaveaLab: look at kb-qa) | Can describe both codebases at a module level |

**Checkpoint**: End of Month 2 -- team lead review. PRs passing with minimal feedback? Contributing meaningfully to reviews?

### Days 61-90: Contribution and Context

| Activity | Success Criteria |
|----------|-----------------|
| Contribution outside initial area | Successful PR in an area not originally assigned |
| Use `/explain` or `/research` skill autonomously | Produces a useful explanation or research log |
| Participate in a design or planning discussion | Offers an informed opinion grounded in project conventions |
| Read recent plan history (`_output/plans/` latest 3 plans) | Can trace a feature from plan to code |

**Checkpoint**: End of Month 3 -- structured review with buddy or team lead. Is the contributor independently productive? Are PRs approved with zero or minimal style/convention feedback?

---

## Recommended Reading List

### Read First (Day 1) -- 5 files

1. `CLAUDE.md` -- project overview, stack, build commands, key conventions
2. `product-design/project/constitution.md` -- immutable principles; understand T1-T5, Q1-Q3, S1-S3
3. `product-design/conventions.md` -- all directory variables and source paths used by skills and references
4. `product-design/project/standards.md` -- engineering standards: module responsibilities, naming, logging, testing
5. `product-design/project/product-design-as-coded.md §0 and §1` -- GaveaLab PoC overview and kb-qa platform purpose

### Read This Week (Week 1) -- 7 files

6. `product-design/project/product-design-as-intended.md §§ 1-3, 8, 13` -- design philosophy, entity hierarchy, UX patterns, user stories
7. `src/kb_qa/constants.py` -- single source of truth for all kb-qa constants
8. `src/kb_qa/ingest.py` -- ingestion pipeline; see `_doc_id()` and the upsert loop
9. `src/kb_qa/query.py` -- retrieval logic; see `KbQa` class and `retrieve()`
10. `gavealab-poc/gavealab_poc/llm.py` -- OllamaClient; understand the single LLM entry point
11. `gavealab-poc/gavealab_poc/workspace.py` -- `GaveaLabWorkspace`; understand the single DB entry point
12. `agents/mcp_server.py` -- FastMCP server; understand the MCP tool boundary and `n_results` cap

### Read This Month (Month 1) -- additional depth

13. `gavealab-poc/gavealab_poc/pipeline/topics.py` -- topic tree generation; study `_extract_json` and `_parse_taxonomy`
14. `gavealab-poc/gavealab_poc/pipeline/claims.py` -- claim extraction pipeline
15. `gavealab-poc/gavealab_poc/pipeline/cruxes.py` -- divergence detection; study the embedding + centroid + LLM pattern
16. `gavealab-poc/gavealab_poc/pipeline/umap_viz.py` -- UMAP cluster visualization; study `build_umap_df`
17. `src/kb_qa/loader.py` -- document loading; understand the `.md` and `.pdf` paths
18. `tests/` -- all test files; understand the `tmp_path` fixture pattern and mock strategy
19. `product-design/project/product-design-as-intended.md §§ Decisions` -- D-001 through D-003: ChromaDB, MCP, embedding model choices
20. `_output/plans/` -- read the most recent 2-3 plans to understand how implementation decisions are documented

---

## Appendix: Key Contacts

| Role | Name | Contact | Topics |
|------|------|---------|--------|
| Buddy/Mentor | _TBD_ | | Day-to-day questions, first PR reviews |
| Tech Lead | _TBD_ | | Architecture decisions, design trade-offs |
| Product Owner | _TBD_ | | Requirements, priorities, user goals |
| QA Lead | _TBD_ | | Testing strategy, quality gates |
| Course Instructor | _TBD_ | | Academic requirements, course milestones |
