.PHONY: install api app dev test lint

install:
	uv sync

api:
	uv run uvicorn fala_gavea.presentation.api.main:app --reload --port 8000

app:
	uv run streamlit run app.py

dev:
	$(MAKE) -j2 api app

test:
	uv run pytest

lint:
	uv run ruff check src/ tests/
