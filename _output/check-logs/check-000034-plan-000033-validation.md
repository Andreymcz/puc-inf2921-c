# Check 000034 | CHORE-all | 2026-06-11 11:55 UTC | Validation Report

## Scope: all (plan-000033 changes)

## Summary

| Check | Status | Errors | Warnings |
|-------|--------|--------|----------|
| ruff (lint) | PASS | 0 | 0 |
| pyright (type check) | FAIL | 15 | 0 |
| pytest (tests) | PASS | 0 | 2 (deprecation) |

**Overall: 2/3 checks passed**

## Notes

### pyright (15 errors — all pre-existing)
All 15 errors are in `sqlalchemy_citizen_post_repository.py` and are pre-existing SQLAlchemy 1.x legacy `Column[T]` typing issues. Baseline at plan start was 20 errors; this plan reduced it to 15. No new errors introduced.

Root cause: `CitizenPostModel` uses untyped `Column` instead of SQLAlchemy 2.0 `Mapped[T]` / `mapped_column()`. Migration to `Mapped[]` style would clear all 15.

### pytest (29 tests pass)
2 deprecation warnings:
- `StarletteDeprecationWarning`: httpx + starlette testclient deprecated; install httpx2
- `DeprecationWarning`: `HTTP_422_UNPROCESSABLE_ENTITY` renamed in newer FastAPI/Starlette

Both are non-blocking.
