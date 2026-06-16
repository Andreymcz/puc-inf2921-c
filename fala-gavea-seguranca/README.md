# Fala Gavea Seguranca

Clean-architecture Python REST API — FastAPI + SQLAlchemy + SQLite + Pydantic v2.

## Stack

- **Python** 3.13 | **FastAPI** | **SQLAlchemy** (sync) | **Pydantic v2** | **SQLite**
- **Tests**: pytest + httpx TestClient
- **Tooling**: uv + ruff

## Quick Start

```bash
uv sync --extra dev
uv run pytest -v
uv run uvicorn fala_gavea_seguranca.presentation.api.main:app --reload
```

## Architecture

```
src/fala_gavea_seguranca/
├── domain/           # Entities, repository interfaces, exceptions (stdlib only)
├── application/      # Use cases (domain only, no I/O)
├── infrastructure/   # SQLAlchemy models + concrete repository
└── presentation/     # FastAPI app, routers, Pydantic schemas
```

## API

| Method | Path | Status |
|--------|------|--------|
| POST   | /security_reports | 201 |
| GET    | /security_reports | 200 |
| GET    | /security_reports/{id} | 200 / 404 |
| DELETE | /security_reports/{id} | 204 / 404 |

## Environment

Copy `.env.example` to `.env` and adjust as needed.
