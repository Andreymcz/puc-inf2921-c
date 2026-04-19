# SECURITY CHECKLISTS — INF2921 Grupo C

---

## Quick Reference — Validation Constants

| Field | Value | Source |
|-------|-------|--------|
| Max file size (ingest) | 50 MB | `src/kb_qa/constants.py` |
| Chunk size | defined in constants.py | `src/kb_qa/constants.py` |

---

## Checklist A — New CLI Command

- [ ] No shell injection via user-supplied file paths — use `pathlib.Path`, never `os.system`
- [ ] File path validated before opening (exists, is a file, readable)
- [ ] File extension validated against allowed types (.md, .pdf)
- [ ] No secrets printed to stdout/stderr in verbose mode

## Checklist B — MCP Tool Exposure

- [ ] Input parameters validated before passing to query.py
- [ ] No internal error details (stack traces) returned in MCP tool response
- [ ] Query string length bounded to prevent unreasonably large embeddings

## Checklist C — Secrets & Credentials

- [ ] Anthropic API key loaded from environment variable or `.env` — never hardcoded
- [ ] `.env` files listed in `.gitignore`
- [ ] `knowledge/vectorstore/` listed in `.gitignore` (contains embedded data)
- [ ] No PUC-Rio proprietary materials committed without approval

## Checklist D — Dependencies

- [ ] New dependencies added to `pyproject.toml` with minimum version pins
- [ ] `uv lock` updated after adding dependencies
- [ ] License compatibility checked for new dependencies

---

## N/A Checklists

The following standard checklists do not apply to this project:

- **Authentication/JWT** — single-user tool, no auth system
- **XSS / HTML sanitization** — no web frontend
- **CSRF** — no web forms
- **File upload via HTTP** — ingest is CLI-only, no HTTP upload
- **SSRF** — no user-supplied URLs fetched by the server
- **Rate limiting** — local tool, no network-exposed endpoints
