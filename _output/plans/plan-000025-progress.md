# Progress -- Plan 000025

Append-only cross-iteration learnings. Each subagent reads this file at the start and appends findings at the end.

## Codebase Patterns

- scaffold.py uses `string.Template` with `${var}` syntax; FastAPI path params `/{id}` have no `$` prefix so they pass through unmodified.
- conftest.py sets `os.environ["DATABASE_URL"] = "sqlite:///:memory:"` BEFORE any package imports so `session.py` picks up in-memory DB at module load.
- `create_app()` calls `create_tables()` which is safe in tests because the env var override makes it use in-memory SQLite.
- The SQLAlchemy repository receives an injected `Session` (not creates its own) for testability.

## Iteration Log
