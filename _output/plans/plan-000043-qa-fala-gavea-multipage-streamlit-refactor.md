# QA Log — plan-000043 | fala-gavea multipage Streamlit refactor | 2026-06-12 11:44 UTC

**Brief:** multipage app with streamlit pages https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
**Skill:** plan
**Plan:** plan-000043

---

## Q&A Log

**Q:** What is the current structure of fala-gavea/app.py?

**A:** `fala-gavea/app.py` is a 413-line monolith containing: module-level constants (`API_URL`, `POSTS_PER_PAGE`), `_CITIZEN_NAMES` list, `citizen_name()` helper, `api_get()` / `api_post()` helpers, and 5 inline page functions (`page_posts`, `page_new_post`, `page_label_feedback`, `page_dashboard`, `page_clusters`). Navigation uses `st.radio` in the sidebar.

**Q:** What multipage approach should be used?

**A:** `st.navigation()` + `st.Page()` (Streamlit 1.28+ programmatic API), consistent with `gavealab-poc/app.py` which already uses this pattern. Each page becomes a module under `fala-gavea/app_pages/` with a `render() -> None` function. Shared utilities move to `app_pages/shared.py`.

**Q:** How is the implicit `USER_ID` global handled after the refactor?

**A:** `USER_ID` is a module-level global in `app.py` built from `st.session_state.user_id`. After the refactor, each page module reads `st.session_state.user_id` directly — no parameter passing needed since Streamlit session state is global within a session.

**Q:** Does `app_pages` need to be declared in `pyproject.toml`?

**A:** No. `app_pages/` is a plain Python package in `fala-gavea/` (not pip-installed). Streamlit runs `app.py` from the `fala-gavea/` directory, so `import app_pages.posts` resolves by standard Python path. Only `src/fala_gavea` is packaged via hatchling (as declared in `pyproject.toml`).

**Q:** What happens to the sidebar title/caption/divider?

**A:** `st.navigation()` renders its own page list in the sidebar automatically. Custom sidebar content (title `🗣️ Fala Gávea`, session caption, divider) can be added after `st.navigation()` is created and before `pg.run()` using a `with st.sidebar:` block.
