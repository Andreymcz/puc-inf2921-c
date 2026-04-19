# PROJECT CONSTITUTION — INF2921 Grupo C

INF2921 Grupo C — Local RAG knowledge base for course INF2921/CIS2114 (AI Systems Design 2026.1), storing and retrieving team knowledge via MCP-compatible AI assistants.

Users are the five-member course team (engineers, a production engineer, a social scientist, and a designer) who use this tool to query accumulated course knowledge during their AI assistant sessions.

---

## Technical Principles

| # | Principle | Rationale |
|---|-----------|-----------|
| T1 | All document ingestion goes through `src/kb_qa/ingest.py` — no direct ChromaDB writes from other modules | Ensures a single, testable ingest path; prevents inconsistent embeddings |
| T2 | All query logic goes through `src/kb_qa/query.py` — the MCP server must not query ChromaDB directly | Keeps retrieval logic testable and decoupled from the MCP transport layer |
| T3 | No secrets or API keys in source code — all credentials come from environment variables | Prevents credential leaks; the Anthropic API key must never be committed |

---

## Quality Principles

| # | Principle | Rationale |
|---|-----------|-----------|
| Q1 | Each source module must have a corresponding test file in `tests/` | Regression prevention for a tool used across five team members |
| Q2 | Vector store files (`knowledge/vectorstore/`) must not be committed to git | Binary store files are large and environment-specific |

---

## Security Invariants

| # | Invariant | Rationale |
|---|-----------|-----------|
| S1 | API keys and secrets must come from environment variables or `.env` files — never hardcoded | Prevents accidental credential exposure in the course repository |
| S2 | `.env` files must be listed in `.gitignore` | Course repo is shared; credentials must not be publicly visible |

---

## Compliance Requirements

| # | Requirement | Regulation/Contract |
|---|-------------|---------------------|
| C1 | No PUC-Rio proprietary course materials may be committed to the public repository without instructor approval | Academic integrity / institutional policy |

---

## Enforcement

- These principles are loaded into every agent context via pre-skill.
- `/check validate` verifies conformance against the agent-facing constraints derived from this document.
- Violations discovered during `/check review` or `/check preflight` are classified as **blocking** — they must be resolved before commit.
- To amend this constitution, the change must be explicitly approved by the project lead and documented in the changelog below.

---

## Changelog

### v1 — 2026-04-19 00:00 UTC
- Initial constitution created via `/design`.
