# PROJECT CONVENTIONS — INF2921 Grupo C

> Centralized project-specific definitions. All skills and reference files reference variables from this file instead of hardcoding project-specific values.

---

## Project Identity

| Variable | Value | Description |
|----------|-------|-------------|
| `PROJECT_NAME` | INF2921 Grupo C | Project display name |
| `PROJECT_DESCRIPTION` | Local RAG knowledge base for course INF2921/CIS2114 — AI Systems Design 2026.1, ingesting documents into ChromaDB and exposing query_knowledge via MCP to AI assistants | One-line project description |
| `PROJECT_MODE` | brownfield | Project mode: brownfield (existing codebase) |

---

## Directory Structure

| Variable | Value | Description |
|----------|-------|-------------|
| `SKILLS_DIR` | `.claude/skills` | Root directory for skill definitions |
| `AGENT_SPECS_DIR` | `project/agent` | Agent-facing structured specifications in YAML (in `_references/`) |
| `OUTPUT_DIR` | `_output` | Root directory for all generated artifacts |
| `PLANS_DIR` | `${OUTPUT_DIR}/plans` | Plan output folder |
| `SCRIPTS_DIR` | `${OUTPUT_DIR}/generated-scripts` | Script output folder |
| `ADVISORY_DIR` | `${OUTPUT_DIR}/advisory-logs` | Advisory log output folder |
| `PROPOSALS_DIR` | `${OUTPUT_DIR}/proposals` | Lightweight change proposals |
| `INVENTORIES_DIR` | `${OUTPUT_DIR}/inventories` | Inventory output folder |
| `USER_TESTS_DIR` | `${OUTPUT_DIR}/user-tests` | User test plan output folder |
| `EXPLAINED_BEHAVIORS_DIR` | `${OUTPUT_DIR}/explained-behaviors` | Behavior explanation output folder |
| `EXPLAINED_CODE_DIR` | `${OUTPUT_DIR}/explained-code` | Code explanation output folder |
| `EXPLAINED_DATA_MODEL_DIR` | `${OUTPUT_DIR}/explained-data-model` | Data model explanation output folder |
| `EXPLAINED_ARCHITECTURE_DIR` | `${OUTPUT_DIR}/explained-architecture` | Architecture explanation output folder |
| `BEHAVIOR_EVOLUTION_DIR` | `${OUTPUT_DIR}/behavior-evolution` | Behavior evolution explanation output folder |
| `REFLECTIONS_DIR` | `${OUTPUT_DIR}/reflections` | Reflection report output folder |
| `ONBOARDING_PLANS_DIR` | `${OUTPUT_DIR}/onboarding-plans` | Onboarding plan output folder |
| `COMMUNICATION_DIR` | `${OUTPUT_DIR}/communication` | Communication material output folder |
| `ROADMAP_DIR` | `${OUTPUT_DIR}/roadmaps` | Roadmap output folder |
| `QA_LOGS_DIR` | `${OUTPUT_DIR}/qa-logs` | QA session log output folder |
| `CHECK_LOGS_DIR` | `${OUTPUT_DIR}/check-logs` | Check/preflight/review output folder |
| `TMP_DIR` | `${OUTPUT_DIR}/tmp` | Temporary/helper scripts |
| `CODEBASE_DIR` | `.` | Root directory of the project codebase |

---

## Key Files

| Variable | Value | Description | Maintained by |
|----------|-------|-------------|--------------|
| `BRIEFS_FILE` | `${OUTPUT_DIR}/briefs.md` | Execution log of all skill invocations | Agent |
| `BRIEFS_INDEX_FILE` | `${OUTPUT_DIR}/briefs-index.md` | Lightweight briefs index (one-line summaries) | Agent |
| `ARTIFACT_INDEX_FILE` | `${OUTPUT_DIR}/INDEX.md` | Single global artifact index | Agent |
| `CONSTITUTION_FILE` | `project/constitution.md` | Project constitution — immutable principles (in `_references/`) | Human |
| `AS_CODED` | `project/product-design-as-coded.md` | Unified implementation state: Conceptual Design, Metacommunication, Journey Maps (in `_references/`) | Agent |
| `CD_AS_IS_CHANGELOG` | `project/product-design-changelog.md` | As-built conceptual design changelog (in `_references/`) | Agent |
| `DESIGN_INTENT` | `project/product-design-as-intended.md` | Unified working intent (§0-§17) + ADR Decision log + CHANGELOG (in `_references/`) | Human (markers) |
| `DESIGN_INTENT_TO_BE` | `project/product-design-as-intended.md` | Legacy alias for `DESIGN_INTENT` | Human (markers) |
| `UX_RESEARCH` | `project/ux-research-results.md` | UX research: personas, problem scenarios, journeys, CHANGELOG (in `_references/`) | Human (markers) |
| `STANDARDS` | `project/standards.md` | Unified engineering standards: Backend, Testing (in `_references/`) | Human / Agent |
| `DESIGN_STANDARDS` | `project/design-standards.md` | Unified design standards (in `_references/`) | Human / Agent |
| `SESSION_NOTES_FILE` | `${TMP_DIR}/session-notes.md` | Session-scoped working memory | Agent |
| `DECISION_DIGEST_FILE` | `${OUTPUT_DIR}/decision-digest.jsonl` | Machine-readable decision index | Agent |

---

## As-Intended / As-Coded Registry

| As-Intended file | Section | As-Coded counterpart |
| ---------------- | ------- | -------------------- |
| `${DESIGN_INTENT}` | §0-§17 design intent + Decisions + CHANGELOG | `${AS_CODED}` |
| `${DESIGN_INTENT}` | §15 designed journeys | `${AS_CODED} § Journey Maps` |
| `${UX_RESEARCH}` | all (personas, scenarios, journeys, CHANGELOG) | `-` |

---

## Review Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `MINIMUM_REVIEW_DEPTH` | `light` | Minimum review depth floor. Valid values: `light`, `standard`, `deep`. |

---

## Periodic Triggers

| Trigger | Interval (days) | Action type | Description |
|---------|-----------------|-------------|-------------|
| Periodic curation | 30 | `periodic-curation` | Review `product-design-as-intended.md` for items ready to promote |
| Spec-drift check | 14 | `spec-drift-check` | Run `/explain spec-drift` to surface drift |

| Threshold | Value | Description |
|-----------|-------|-------------|
| Verify-as-coded file threshold | 5 | Minimum files changed before post-skill creates a `verify-as-coded` action |
| Pending age escalation | 14 | Days before a pending action is flagged "overdue" |
| Pending auto-dismiss | 90 | Days after which unaddressed pending actions are auto-dismissed |

---

## Source Directories

| Variable | Value | Description |
|----------|-------|-------------|
| `BACKEND_DIR` | `src` | Backend source root |
| `FRONTEND_DIR` | N/A | Frontend source root (no frontend) |
| `BACKEND_FRAMEWORK` | `none` | No HTTP framework — Python CLI + MCP server |
| `FRONTEND_FRAMEWORK` | `none` | No frontend framework |

---

## Stack Description

| Variable | Value | Description |
|----------|-------|-------------|
| `BACKEND_STACK` | Python 3.13 + ChromaDB + sentence-transformers + MCP CLI + Anthropic SDK + Click | Backend technology summary |
| `FRONTEND_STACK` | N/A | No frontend |
| `TESTING_STACK` | pytest | Testing technology summary |
| `DEPLOYMENT_STACK` | uv (local) | Local development and deployment |

---

## Architecture Description

| Variable | Value | Description |
|----------|-------|-------------|
| `ARCHITECTURE_DESCRIPTION` | Python CLI + MCP server exposing RAG query over ChromaDB vector store. Documents (.md, .pdf) are ingested via CLI and embedded into ChromaDB. The MCP server exposes `query_knowledge` for AI assistants (Claude, Copilot). | High-level architecture description |
| `ARCHITECTURE_PATTERN` | Pipeline: CLI Ingest → Embed (sentence-transformers) → Store (ChromaDB) → MCP Query | Architecture pattern |
| `BACKEND_ARCHITECTURE_SUMMARY` | Python package (src/kb_qa) with CLI entry point (Click) and MCP server (agents/mcp_server.py). Modules: cli, ingest, loader, query, constants. | Backend architecture summary |
| `FRONTEND_ARCHITECTURE_SUMMARY` | N/A | No frontend |
| `MODELS_DIR` | N/A | No ORM models (ChromaDB vector store only) |
| `CONVENTION_1` | All document ingestion goes through src/kb_qa/ingest.py — no direct ChromaDB writes from other modules | Key project convention #1 |
| `CONVENTION_2` | All query logic goes through src/kb_qa/query.py — exposed via MCP server in agents/mcp_server.py | Key project convention #2 |
| `CONVENTION_3` | Vector store files live in knowledge/vectorstore — not committed to git | Key project convention #3 |

---

## Backend Structure

| Variable | Value | Description |
|----------|-------|-------------|
| `BACKEND_APP_DIR` | `src/kb_qa` | Main package root |
| `BACKEND_CONSTANTS_FILE` | `src/kb_qa/constants.py` | Constants file |
| `MIGRATIONS_DIR` | N/A | No SQL migrations (ChromaDB) |
| `TRANSLATIONS_DIR` | N/A | No i18n translations |

---

## i18n Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `I18N_FRONTEND_FILES` | N/A | No frontend locales |
| `I18N_BACKEND_CATALOGS` | N/A | No backend i18n catalogs |

---

## Test Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `BACKEND_SUBPACKAGES` | `kb_qa` | Backend subpackage for coverage grouping |
| `FRONTEND_SUBPACKAGES` | N/A | No frontend |
| `FRONTEND_ENTRY_POINTS` | N/A | No frontend entry points |

---

## Secret Scanning

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRETS_EXTRA_SKIP_PATTERNS` | | Additional filename substrings to skip |
| `SECRETS_EXTRA_SKIP_DIRS` | `knowledge/vectorstore` | Skip vector store binary files |
| `SECRETS_EXTRA_SKIP_EXTENSIONS` | `.bin,.sqlite3` | Skip binary and database files |
| `SECRETS_EXTRA_FALSE_POSITIVES` | | Additional false-positive patterns |
| `SECRETS_EXTRA_PATTERNS` | | Additional secret-detection patterns |

---

## Build & Test Commands

| Variable | Value | Description |
|----------|-------|-------------|
| `ALL_TESTS_CMD` | `uv run pytest` | Command to run all tests |
| `BACKEND_TEST_CMD` | `uv run pytest` | Command to run backend tests |
| `BACKEND_INTEGRATION_TEST_CMD` | `uv run pytest tests/integration` | Command to run integration tests |
| `BACKEND_TEST_FILE_CMD` | `uv run pytest {file}` | Command to run a single test file |
| `FRONTEND_TEST_CMD` | N/A | No frontend tests |
| `FRONTEND_TEST_FILE_CMD` | N/A | No frontend tests |
| `E2E_TEST_CMD` | N/A | No E2E tests |
| `MIGRATION_CHAIN_SCRIPT` | N/A | No SQL migrations |
