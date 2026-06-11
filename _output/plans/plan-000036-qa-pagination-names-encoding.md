# QA Log | Plan 000036 | 2026-06-11 16:51 UTC | fala-gavea posts pagination, citizen names, encoding fix

**Brief:** Plan session for three improvements to the Fala Gávea Streamlit app: fix CSV encoding bug in seed_db.py, add human-readable citizen names, and implement posts pagination.

---

## Q1
add paginaçao das postagens, inventar nomes melhores para os cidadaos, fix problema com encoding: "A situaÃ§Ã£o da saÃºde aqui tÃ¡ precÃ¡ria demais. "

## A1
Ran pre-skill, inspected `fala-gavea/app.py`, `scripts/seed_db.py`, the CSV file, and the FastAPI router to understand the current state. Identified three issues:

1. **Encoding**: `seed_db.py` opens the CSV with `encoding="latin-1"` but the file is UTF-8 — classic Mojibake. Fix: change to `encoding="utf-8"`.
2. **Citizen names**: Posts show raw UUIDs truncated to 8 chars. Fix: add a deterministic `citizen_name()` function using MD5 hash to pick from 30 Brazilian first names.
3. **Pagination**: `page_posts()` fetches up to 100 posts at once. The backend already supports `limit` + `offset`. Fix: add Streamlit session state pagination with 20 posts per page and prev/next controls.

Generated **plan-000036** with 4 steps covering all three changes in `fala-gavea/scripts/seed_db.py` and `fala-gavea/app.py`. Filed implement pending entry `pa-000025`.
