---
designer_description: "Security checklists for kb-qa — dependency scanning, secret management, and logging hygiene for a local CLI/MCP tool."
---

# SECURITY CHECKLISTS — INF2921-Grupo-C / kb-qa

> **Scope note**: kb-qa is a local, single-user CLI/MCP tool with no web server, no authentication, and no database. Most standard web-security checklists (endpoints, CSRF, CORS, XSS, auth) do not apply. Relevant surfaces: dependency security, secret management, logging hygiene, and document privacy.

---

## Checklist A — New CLI Command or MCP Tool

- [ ] Command/tool is read-only (preferred) or has an explicit `--confirm` / `--force` flag for destructive operations
- [ ] All path arguments validated to exist and be within expected directories — no path traversal
- [ ] User-supplied strings passed to ChromaDB queries, not interpolated into system commands
- [ ] Error messages do not expose internal stack traces to the end user
- [ ] `n_results` or equivalent is capped at 20 (MCP boundary)

---

## Checklist B — Dependency Security

- [ ] `uv run pip-audit` (or equivalent) run against locked dependencies before each release
- [ ] No known critical or high-severity CVEs in production dependencies at release time
- [ ] `uv.lock` committed for reproducible builds
- [ ] Dependencies reviewed after each major ChromaDB, sentence-transformers, or mcp release
- [ ] `anthropic` SDK kept up to date (security patches released frequently)

---

## Checklist C — Secret Management

- [ ] `.env` files listed in `.gitignore` — never committed
- [ ] Any Anthropic API keys come from environment variables, not source code
- [ ] `knowledge/vectorstore/` is gitignored — vector store not committed
- [ ] Pre-commit hook or CI step scans for secret patterns (`.claude/skills/scripts/check_secrets.py`)
- [ ] Any secret accidentally committed is rotated immediately

---

## Checklist D — Document Privacy

- [ ] `knowledge/` directory reviewed before running `git add` — ensure no sensitive documents are tracked
- [ ] `.gitignore` covers `knowledge/vectorstore/` and any other derived artifacts
- [ ] Documents containing PII or proprietary information placed in `knowledge/` only when the repository is private or the knowledge/ directory is explicitly excluded from git tracking
- [ ] MCP query responses (retrieved text chunks) pass through the AI provider's inference infrastructure — users aware that retrieved content leaves the local machine via the LLM query

---

## Checklist E — Logging Security

- [ ] Log messages never contain API keys, passwords, or tokens
- [ ] Document content not logged at DEBUG or higher by default (chunks can be large and sensitive)
- [ ] Log format strings are not user-controlled
- [ ] No `print()` statements in production code paths — use `logging` module

---

## Quick Reference — Validation Constants

| Constant | Backend | Value | Defined in |
| -------- | ------- | ----- | ---------- |
| `n_results` max (MCP) | `agents/mcp_server.py` | 20 | `min(n_results, 20)` inline |
| `EMBED_BATCH_SIZE` | `src/kb_qa/constants.py` | 256 | `EMBED_BATCH_SIZE` |
| Supported document types | `src/kb_qa/constants.py` | `{"md", "pdf"}` | `DOCUMENT_TYPES` |

No frontend constants — CLI/MCP-only tool.
