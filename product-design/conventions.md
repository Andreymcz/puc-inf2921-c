---
designer_description: "Single source of truth for directory structure, stack, test commands, and the registry of as-intended / as-coded files for INF2921-Grupo-C."
---

# PROJECT CONVENTIONS — INF2921-Grupo-C

> Centralized project-specific definitions. All skills and reference files reference variables from this file instead of hardcoding project-specific values.

---

## Project Identity

| Variable | Value | Description |
|----------|-------|-------------|
| `PROJECT_NAME` | INF2921-Grupo-C | Project display name |
| `PROJECT_DESCRIPTION` | Generic RAG knowledge base — ingest .md and .pdf files into ChromaDB and expose query_knowledge via MCP | One-line project description |
| `PROJECT_MODE` | brownfield | Project mode: brownfield (existing codebase) |

---

## Directory Structure

| Variable | Value | Description |
|----------|-------|-------------|
| `SKILLS_DIR` | `.claude/skills` | Root directory for skill definitions |
| `AGENT_SPECS_DIR` | `project/agent` | Agent-facing structured specifications in YAML (in `product-design/`) |
| `OUTPUT_DIR` | `_output` | Root directory for all generated artifacts |
| `PLANS_DIR` | `${OUTPUT_DIR}/plans` | Plan output folder |
| `SCRIPTS_DIR` | `${OUTPUT_DIR}/generated-scripts` | Script output folder |
| `ADVISORY_DIR` | `${OUTPUT_DIR}/advisory-logs` | Legacy advisory log output folder |
| `RESEARCH_DIR` | `${OUTPUT_DIR}/research-logs` | Research log output folder |
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
| `CODEBASE_DIR` | `.` | Root directory of the project codebase (embedded mode) |

---

## Key Files

| Variable | Value | Description | Maintained by |
|----------|-------|-------------|--------------|
| `BRIEFS_FILE` | `${OUTPUT_DIR}/briefs.md` | Execution log of all skill invocations | Agent |
| `BRIEFS_INDEX_FILE` | `${OUTPUT_DIR}/briefs-index.md` | Lightweight briefs index (one-line summaries) | Agent |
| `ARTIFACT_INDEX_FILE` | `${OUTPUT_DIR}/INDEX.md` | Single global artifact index | Agent |
| `CONSTITUTION_FILE` | `project/constitution.md` | Project constitution — immutable principles (in `product-design/`) | Human |
| `AS_CODED` | `project/product-design-as-coded.md` | Unified implementation state (in `product-design/`) | Agent |
| `CD_AS_IS_CHANGELOG` | `project/product-design-changelog.md` | As-built conceptual design changelog (in `product-design/`) | Agent |
| `DESIGN_INTENT` | `project/product-design-as-intended.md` | Unified working intent + Decisions + CHANGELOG (in `product-design/`) | Human (markers) |
| `DESIGN_INTENT_TO_BE` | `project/product-design-as-intended.md` | Legacy alias for `DESIGN_INTENT` | Human (markers) |
| `UX_RESEARCH` | `project/ux-research-results.md` | UX research: personas, problem scenarios, journeys (in `product-design/`) | Human (markers) |
| `STANDARDS` | `project/standards.md` | Unified engineering standards (in `product-design/`) | Human / Agent |
| `DECISION_DIGEST_FILE` | `${OUTPUT_DIR}/decision-digest.jsonl` | Machine-readable decision index | Agent |
| `CONVERSATION_TRACE_FILE` | `${OUTPUT_DIR}/conversation-trace.jsonl` | Append-only conversation trace log | Agent |

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
| Git freshness check | 7 | `check-git-freshness` | Compare each project git repo to its upstream |

| Threshold | Value | Description |
|-----------|-------|-------------|
| Pending plan age escalation | 30 | Days before an open `implement` pending entry is surfaced with the overdue banner |
| Verify-as-coded file threshold | 5 | Minimum number of files changed by a plan before post-skill auto-creates a `verify-as-coded` pending action |
| Pending age escalation | 14 | Days before a pending action is flagged "overdue" |
| Pending auto-dismiss | 90 | Days after which unaddressed pending actions are auto-dismissed |

---

## Source Directories

> CLI/library project — no backend web framework, no frontend.

| Variable | Value | Description |
|----------|-------|-------------|
| `SRC_DIR` | `src/kb_qa` | Main package source root |

---

## Stack Description

| Variable | Value | Description |
|----------|-------|-------------|
| `TESTING_STACK` | pytest | Testing technology summary |
| `DEPLOYMENT_STACK` | local / NAS pessoal | Deployment technology summary |

---

## Architecture Description

| Variable | Value | Description |
|----------|-------|-------------|
| `ARCHITECTURE_DESCRIPTION` | Python CLI tool (click) + MCP server exposing query_knowledge over a ChromaDB vector store built from .md and .pdf documents via sentence-transformers | High-level architecture description |
| `ARCHITECTURE_PATTERN` | Module-based CLI + MCP adapter | Architecture pattern |
| `CONVENTION_1` | All document ingestion goes through src/kb_qa/ingestion/ — no ad-hoc file reading elsewhere | Key project convention #1 |
| `CONVENTION_2` | The vector store lives at knowledge/vectorstore/ and is gitignored | Key project convention #2 |
| `CONVENTION_3` | Type annotations required on all public functions; no hardcoded paths | Key project convention #3 |

---

## Secret Scanning

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRETS_EXTRA_SKIP_PATTERNS` | | Additional filename substrings to skip during secret scanning |
| `SECRETS_EXTRA_SKIP_DIRS` | knowledge/vectorstore | Additional directory names to skip during secret scanning |
| `SECRETS_EXTRA_SKIP_EXTENSIONS` | | Additional file extensions to skip |
| `SECRETS_EXTRA_FALSE_POSITIVES` | | Additional false-positive regex patterns |
| `SECRETS_EXTRA_PATTERNS` | | Additional secret-detection regex patterns |

---

## Build & Test Commands

| Variable | Value | Description |
|----------|-------|-------------|
| `ALL_TESTS_CMD` | uv run pytest | Command to run all tests |
