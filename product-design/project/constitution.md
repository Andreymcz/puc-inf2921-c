---
designer_description: "Immutable principles for INF2921-Grupo-C / GaveaLab — loaded by every skill before any other reference."
---

# PROJECT CONSTITUTION — INF2921-Grupo-C / GaveaLab

INF2921-Grupo-C — GaveaLab citizen feedback analysis tool (primary deliverable) + kb-qa local RAG supporting tool. Designed for the INF2921/CIS2114 AI Systems Design course (2026.1, PUC-Rio). Team: Andrey, Mauro, Julia, Herbert, Natali e Sheila.

---

## Technical Principles

### GaveaLab (primary product)

| # | Principle | Rationale |
|---|-----------|-----------|
| T1 | All LLM calls go through `gavealab_poc/llm.py` (OllamaClient) — no direct httpx or openai calls in pipeline or page modules | Centralizes model configuration and makes model swaps a one-line change |
| T2 | All SQLite access goes through `GaveaLabWorkspace` — pipeline and page modules never access the database directly | Maintains a single auditable persistence path; prevents schema divergence |
| T3 | Type annotations required on all public functions; LLM model URL and name come from env vars only (`GAVEALAB_OLLAMA_URL`, `GAVEALAB_OLLAMA_MODEL`) | Enables pyright checking; ensures environment-portability without code changes |
| T4 | `gavealab.db` is gitignored — never committed | Citizen data and analysis results are private derived artifacts, not source files |
| T5 | The Streamlit `GaveaLabWorkspace` instance is created via `@st.cache_resource` — exactly one instance per app process | Prevents multiple open SQLite connections and race conditions across page rerenders |

### kb-qa (supporting tool — stable)

| # | Principle | Rationale |
|---|-----------|-----------|
| T6 | All document ingestion goes through `src/kb_qa/ingestion/` — no ad-hoc file reading elsewhere | Maintains a single auditable ingestion path |
| T7 | The vector store lives at `knowledge/vectorstore/` and is gitignored — never committed | Avoids accidental data leakage |
| T8 | `n_results` is always capped at 20 at the MCP boundary | Prevents excessive token usage in downstream LLM consumers |

---

## Quality Principles

| # | Principle | Rationale |
|---|-----------|-----------|
| Q1 | All tests use pytest — no ad-hoc scripts as test replacements | Consistent discovery and coverage reporting via `uv run pytest` |
| Q2 | Ruff linting passes before any commit (`uv run ruff check src/ gavealab-poc/`) | Keeps code style consistent across the team |
| Q3 | Type annotations required on all public functions in both `src/kb_qa` and `gavealab-poc/gavealab_poc` | Catches type errors early |

---

## Security Invariants

| # | Invariant | Rationale |
|---|-----------|-----------|
| S1 | No API keys or credentials in source code — all secrets come from environment variables | Prevents credential leaks in git history |
| S2 | `gavealab.db` and `knowledge/vectorstore/` are gitignored — citizen relatos and document vectors never committed | Prevents accidental exposure of sensitive data |
| S3 | The MCP tool `query_knowledge` is read-only — it does not write, delete, or modify the vector store | Limits blast radius of any MCP client misuse to retrieval only |
| S4 | GaveaLab pipeline modules are read-only with respect to the SQLite database — only `GaveaLabWorkspace` methods may write | Prevents uncoordinated writes from pipeline logic |

---

## Compliance Requirements

| # | Requirement | Regulation/Contract |
|---|-------------|---------------------|
| C1 | Citizen relatos and analysis results never leave the local machine — all LLM inference runs via local Ollama | Privacy-first design principle — data sovereignty for the analyst |
| C2 | User documents (kb-qa) never leave the local machine except through the MCP consumer's explicit query | Privacy-first design principle — data sovereignty for the document owner |

---

## Enforcement

- These principles are loaded into every agent context via pre-skill.
- `/check validate` verifies conformance against the agent-facing constraints derived from this document.
- Violations discovered during `/check review` or `/check preflight` are classified as **blocking** — they must be resolved before commit.
- To amend this constitution, the change must be explicitly approved by the project lead and documented in the changelog below.

---

## Changelog

### v1 — 2026-05-24 00:00 UTC
- Initial constitution created via `/design`.

### v2 — 2026-06-02 00:00 UTC
- Rewritten to reflect GaveaLab as primary product and kb-qa as supporting tool.
- Added T1–T5 for GaveaLab; kb-qa principles renumbered T6–T8.
- Added S4 (GaveaLab write isolation) and C1 (citizen data privacy).
- Updated project description and designer_description.