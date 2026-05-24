---
designer_description: "Immutable principles for INF2921-Grupo-C / kb-qa — loaded by every skill before any other reference."
---

# PROJECT CONSTITUTION — INF2921-Grupo-C / kb-qa

INF2921-Grupo-C / kb-qa — A privacy-first local RAG knowledge base that lets researchers ingest their own documents and query them semantically through Claude and other AI tools.

Designed for the INF2921/CIS2114 AI Systems Design course (2026.1, PUC-Rio). Team: Andrey, Mauro, Julia, Herbert, Natali e Sheila.

---

## Technical Principles

| # | Principle | Rationale |
|---|-----------|-----------|
| T1 | All document ingestion goes through `src/kb_qa/ingestion/` — no ad-hoc file reading elsewhere | Maintains a single auditable ingestion path; prevents undiscovered ingest side-effects |
| T2 | The vector store lives at `knowledge/vectorstore/` and is gitignored — never committed | Avoids accidental data leakage; vector stores are derived artifacts, not source files |
| T3 | Type annotations required on all public functions; no hardcoded paths | Enables pyright static checking; ensures path flexibility via config or CLI arguments |
| T4 | `n_results` is always capped at 20 at the MCP boundary | Prevents excessive token usage in downstream LLM consumers |
| T5 | The embedding model name is defined in `constants.py` only — no inline model names in business logic | Enables centralized model upgrades without hunting scattered strings |

---

## Quality Principles

| # | Principle | Rationale |
|---|-----------|-----------|
| Q1 | All tests use pytest — no ad-hoc scripts as test replacements | Consistent discovery and coverage reporting via `uv run pytest` |
| Q2 | Ruff linting passes before any commit (`uv run ruff check src/`) | Keeps code style consistent across the team |
| Q3 | Pyright type-check passes on the `src/` package | Catches type errors early; supports IDE tooling for all team members |

---

## Security Invariants

| # | Invariant | Rationale |
|---|-----------|-----------|
| S1 | No API keys or credentials in source code — all secrets come from environment variables | Prevents credential leaks in git history |
| S2 | Documents in `knowledge/` are treated as potentially sensitive — the `vectorstore/` path is gitignored | Prevents accidental exposure of user documents via git |
| S3 | The MCP tool `query_knowledge` is read-only — it does not write, delete, or modify the vector store | Limits blast radius of any MCP client misuse to retrieval only |

---

## Compliance Requirements

| # | Requirement | Regulation/Contract |
|---|-------------|---------------------|
| C1 | User documents never leave the local machine except through the MCP consumer's explicit query | Privacy-first design principle — data sovereignty for the document owner |

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