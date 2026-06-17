# Check 000073 | CHORE-all | 2026-06-17 17:47 UTC | Validation Report — fala-gavea scaffold

**Scope:** `fala-gavea/` (post-scaffold validation)
**Project:** fala-gavea — FastAPI + SQLite clean architecture

---

## Summary

| Check | Status | Notes |
|-------|--------|-------|
| pytest (18 tests) | ✅ PASS | 18 passed, 0 failed, 2 deprecation warnings (starlette httpx → httpx2; HTTP_422 constant rename — non-blocking) |
| ruff lint (src/ tests/) | ✅ PASS | 5 issues found and fixed (E402 noqa in conftest.py, F401 auto-fixed in test_reports_api.py) |
| Harness structure | ✅ PASS | `.claude/skills/plan/SKILL.md`, `product-design/conventions.md`, `product-design/project/constitution.md`, `CLAUDE.md` all present |
| conventions.md completeness | ✅ PASS | PROJECT_NAME=fala-gavea, SRC_DIR=src/fala_gavea, ALL_TESTS_CMD=uv run pytest, ARCHITECTURE_DESCRIPTION and 3 CONVENTIONs filled |
| .seja-version | ✅ PASS | v0.5.0 |
| uv sync | ✅ PASS | Fixed Windows `greenlet` wheel issue via `[tool.uv] required-environments` |

**Result: 6/6 checks passed.**

---

## Fixes Applied

- `tests/conftest.py`: Added `# noqa: E402` to post-monkey-patch imports (intentional pattern — DB session must be patched before importing ORM models)
- `tests/integration/api/test_reports_api.py`: Removed unused `import pytest` via `ruff --fix`

---

## Deprecation Warnings (advisory, non-blocking)

- `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead` — fix when upgrading deps
- `StarletteDeprecationWarning: 'HTTP_422_UNPROCESSABLE_ENTITY' is deprecated` — starlette constant rename; non-breaking for now
