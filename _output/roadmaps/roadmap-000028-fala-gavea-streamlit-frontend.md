# Roadmap 000028 | 2026-06-11 03:42 UTC | fala-gavea: Streamlit frontend + backend likes/label_feedback

## Brief

App Streamlit em `fala-gavea/app.py` que consome a API REST FastAPI existente. O app tem 4 páginas: Postagens (lista + like), Nova Postagem (formulário), Validar Labels (thumbs up/down em ai_labels), Dashboard (métricas). O backend precisa de novos endpoints para likes (toggle, one-like-per-user) e label_feedback. user_id gerado por sessão via uuid.

## Architecture

- **Backend**: FastAPI existente em `src/fala_gavea/`. Adicionar: `POST /citizen_posts/{id}/likes` (toggle), `DELETE /citizen_posts/{id}/likes` (remover like), `POST /citizen_posts/{id}/label_feedback` (thumbs up/down por label). Persistência de quem curtiu num novo modelo `LikeModel` (SQLAlchemy). `likes_count` derivado do count de LikeModel.
- **Frontend**: `fala-gavea/app.py` (Streamlit, novo arquivo). Dependência: `streamlit>=1.35`, `httpx>=0.27` adicionados ao `pyproject.toml`. Comunica com backend via `http://localhost:8000` (configurável via `FALA_GAVEA_API_URL`).

## Wave Summary

| Wave | Item | Plan | Title | Depends On | Status |
|------|------|------|-------|------------|--------|
| 0 | W0-1 | [plan-000029](../plans/plan-000029-fala-gavea-backend-likes-label-feedback.md) | Backend: likes e label_feedback endpoints | — | pending |
| 1 | W1-1 | [plan-000030](../plans/plan-000030-fala-gavea-app-streamlit.md) | App Streamlit consumindo API REST | W0-1 | pending |
