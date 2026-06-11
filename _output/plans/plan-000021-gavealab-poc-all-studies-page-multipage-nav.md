# DONE | 2026-06-10 00:53 UTC | Plan 000021 | FEATURE-F frontend | 2026-06-09 23:32 | gavealab-poc: all studies page and modern multipage navigation | Review: standard
plan_format_version: 1

## Brief (verbatim)
feature on gavealab-poc: show all studies page and select to view and work on results research for more modert strteamlit features to create a multipage app

## Agent Interpretation
Introduce a dedicated "Todos os Estudos" (All Studies) dashboard page that lists every persisted analysis session with its completion status (which pipeline results exist), and allows the user to open any session directly. Simultaneously refactor `app.py` from `st.sidebar.radio` to the modern `st.navigation()` + `st.Page()` API (available since Streamlit 1.28; project runs 1.58.0), giving each page a proper URL slug and browser-tab title.

## Files
- `gavealab-poc/gavealab_poc/workspace.py` (modify)
- `gavealab-poc/gavealab_poc/pages/all_sessions.py` (create)
- `gavealab-poc/gavealab_poc/pages/upload.py` (modify -- simplify session list)
- `gavealab-poc/app.py` (modify -- navigation refactor)
- `gavealab-poc/tests/test_workspace.py` (create or modify)

## Scope and Constraints
- Streamlit 1.58.0: `st.navigation()` and `st.Page()` are stable. No new dependencies needed.
- `GaveaLabWorkspace` is the only write path (constitution T2). Page modules call `workspace` methods; they never touch SQLite directly.
- All UI strings in pt-BR (standard §i18n).
- `@st.cache_resource` singleton for workspace lives in `app.py` only (constitution T5).
- The upload page retains its upload form; the "Sessoes anteriores" inline list is removed since the dedicated "Todos os Estudos" page now owns that concern.

## Review Log

### ARCH -- Adopted
`app.py` becomes the sole routing host: it defines one zero-arg callable wrapper per page (e.g., `_page_all_sessions()`) that calls `render(get_workspace())`. This preserves the existing `render(workspace: GaveaLabWorkspace) -> None` contract on every page module without touching any of them except `upload.py`. The workspace singleton from `@st.cache_resource` is shared across all wrappers via closure. Layer boundaries unchanged.

### UX -- Adopted
"Todos os Estudos" is placed first in the navigation list (default landing page). Each session card shows: name, date, comment count, and four status badges (Temas / Claims / Divergencias / UMAP -- green when result exists, grey otherwise). An "Abrir" button loads the session and navigates to "Temas automaticos" as the natural next step. A sidebar callout ("Sessao ativa: {name}") visible on all analysis pages replaces the scattered session-load widgets.

### DX -- Adopted
New workspace method `get_sessions_summary()` uses a single SQL query (GROUP BY with conditional aggregation) to return `id, name, created_at, comment_count, available_results` for all sessions -- no N+1 queries.

### TEST -- Adopted
`test_workspace.py` adds tests for `get_sessions_summary()`: empty DB, single session with no results, session with partial results, session with all four result types.

### SEC -- N/A
Local single-user tool, no new attack surfaces. Read-only SQL query.

### I18N -- Adopted
All new UI labels (badge names, button labels, empty-state message) are in pt-BR, consistent with existing pages.

---

## Steps

### Step 1: Add `get_sessions_summary()` to `GaveaLabWorkspace`
Add a method `get_sessions_summary() -> list[dict]` to `GaveaLabWorkspace` in `workspace.py`. Each dict contains: `id: int`, `name: str`, `created_at: str`, `comment_count: int`, `available_results: list[str]`.

Implementation: run one SQL query joining `sessions` (all rows) with `results` (aggregated per session). Use a single SELECT with GROUP_CONCAT (or a follow-up per-session query in Python -- whichever is cleaner given SQLite's limited aggregate functions). Simpler: do two queries -- `list_sessions()` then one `SELECT session_id, result_type FROM results WHERE session_id IN (...)` -- to build the result dict in Python. Parse `comment_count` from `len(csv_raw.splitlines()) - 1` stored inline OR from `_parse_csv` at load time.

Note: `comment_count` requires parsing the CSV. To avoid parsing all CSVs on every dashboard load, store `comment_count` as a new column in the `sessions` table via a migration. Alternatively, compute it cheaply from `csv_raw.count('\n')` (approximate, good enough for display). Use the latter to avoid a schema migration.

- **Files**: `gavealab-poc/gavealab_poc/workspace.py` (modify)
- **References**: `project/standards.md § GaveaLab-Specific Standards`, `project/standards.md § Backend`
- **Interface**: `GaveaLabWorkspace.get_sessions_summary() -> list[dict]` where each dict has keys `id: int`, `name: str`, `created_at: str`, `comment_count: int`, `available_results: list[str]`
- **Verify**: unit tests pass; `uv run pytest gavealab-poc/tests/test_workspace.py -v`
- **Tests**: Add `gavealab-poc/tests/test_workspace.py` with four cases: (1) empty DB returns `[]`; (2) session with no results returns `available_results=[]` and correct `comment_count`; (3) session with `topic_tree` only returns `available_results=["topic_tree"]`; (4) session with all four result types returns all four in `available_results`.
- [x] Done

### Step 2: Create `gavealab_poc/pages/all_sessions.py`
Create `gavealab_poc/pages/all_sessions.py` with a `render(workspace: GaveaLabWorkspace) -> None` function implementing the "Todos os Estudos" dashboard.

Page layout:
- `st.header("Todos os Estudos")`
- If no sessions: `st.info("Nenhuma sessao encontrada. Use a pagina 'Upload CSV' para criar sua primeira analise.")` and return.
- For each session (newest first, from `get_sessions_summary()`): render an `st.container(border=True)` with:
  - Left column: session name (bold), date (caption), `{n} relatos` (caption).
  - Right column: four colored badges using `st.badge()` or inline HTML via `st.markdown`. Badge labels and colors:
    - "Temas" -- green if `"topic_tree"` in `available_results`, grey otherwise
    - "Claims" -- green if `"claims_tree"` in `available_results`
    - "Divergencias" -- green if `"cruxes"` in `available_results`
    - "UMAP" -- green if both `"claims_tree"` (embeddings come from claims) in `available_results`
  - Full-width "Abrir este estudo" button: on click, `st.session_state.session = workspace.load_session(s["id"])` and `st.success(f"Sessao '{s['name']}' carregada. Use a navegacao para continuar a analise.")`.

Note: use `st.columns([3, 2])` for the two-column layout within each container. For badges, since `st.badge()` is Streamlit 1.42+ (available at 1.58.0), use it with `color="green"` or `color="gray"`.

- **Files**: `gavealab-poc/gavealab_poc/pages/all_sessions.py` (create)
- **References**: `project/standards.md § GaveaLab-Specific Standards`, `project/design-standards.md § UX patterns`
- **Depends on**: Step 1
- **Interface**: `render(workspace: GaveaLabWorkspace) -> None`
- **Verify**: page renders without error when launched; shows session list when sessions exist; "Abrir" button sets `st.session_state.session` correctly.
- **Tests**: N/A (Streamlit page rendering is not unit-testable without full Streamlit harness; behavior is covered by workspace tests)
- **Docs**: Update `CLAUDE.md` dev section if needed to mention the new page (only if the section lists pages explicitly)
- [x] Done

### Step 3: Refactor `app.py` to use `st.navigation()` + `st.Page()`
Replace the `st.sidebar.radio` navigation in `app.py` with `st.navigation()` + `st.Page()`. Add a sidebar active-session indicator.

Changes:
1. Define one zero-arg wrapper per page (e.g., `def _page_all_sessions(): from gavealab_poc.pages.all_sessions import render; render(get_workspace())`).
2. Build navigation list:
   ```python
   pages = [
       st.Page(_page_all_sessions, title="Todos os Estudos", icon=":material/home:", default=True),
       st.Page(_page_upload, title="Upload CSV", icon=":material/upload_file:"),
       st.Page(_page_auto_topics, title="Temas automaticos", icon=":material/auto_awesome:"),
       st.Page(_page_manual_topics, title="Categorizar por temas", icon=":material/category:"),
       st.Page(_page_cruxes, title="Opinioes divergentes", icon=":material/compare_arrows:"),
       st.Page(_page_umap_viz, title="Visualizar clusters", icon=":material/scatter_plot:"),
   ]
   pg = st.navigation(pages)
   ```
3. After `st.set_page_config` and before `pg.run()`, add a sidebar active-session indicator:
   ```python
   if st.session_state.get("session"):
       st.sidebar.success(f"Sessao ativa: **{st.session_state.session.name}**")
   else:
       st.sidebar.info("Nenhuma sessao ativa.")
   ```
4. Remove the old `if page == "..."` dispatch block.
5. Remove initialization of `if "session" not in st.session_state` from app.py (Streamlit preserves session_state per browser session; each page wrapper re-checks it as needed). Actually keep the init here since app.py is the entry point -- ensure `st.session_state.session` exists.

Note: `st.set_page_config` must be called before any other Streamlit call. Keep it as the first call in `app.py`.

- **Files**: `gavealab-poc/app.py` (modify)
- **References**: `project/standards.md § GaveaLab-Specific Standards`, `product-design/project/standards.md § Streamlit Conventions`
- **Depends on**: Step 2
- **Interface**: N/A
- **Verify**: `cd gavealab-poc && uv run streamlit run app.py` starts without errors; all six pages appear in the sidebar navigation; "Todos os Estudos" loads as the default page; active session indicator updates when a session is opened.
- **Tests**: N/A
- [x] Done

### Step 4: Simplify `gavealab_poc/pages/upload.py`
Remove the "Sessoes anteriores" block (lines 14-24 in the current file) from `upload.py`. The dedicated "Todos os Estudos" page now owns session listing. Keep the "Nova sessao" upload form unchanged.

Add a `st.info()` hint at the top: `"Para ver e carregar sessoes anteriores, va para Todos os Estudos no menu."` so users know where to find past sessions.

- **Files**: `gavealab-poc/gavealab_poc/pages/upload.py` (modify)
- **References**: `project/standards.md § GaveaLab-Specific Standards`
- **Depends on**: Step 3
- **Interface**: N/A
- **Verify**: Upload page renders cleanly with only the upload form and the navigation hint; no "Sessoes anteriores" section visible.
- **Tests**: N/A
- [x] Done

---

## Commit Message
```
feat(gavealab-poc): add all-studies dashboard and modern multipage nav

- Add GaveaLabWorkspace.get_sessions_summary() with single-query
  session metadata including available result types
- Add pages/all_sessions.py: session cards with status badges and
  one-click session load
- Refactor app.py to st.navigation() + st.Page() (Streamlit 1.28+ API)
  with per-page wrappers and active-session sidebar indicator
- Simplify upload page: remove inline session list (owned by dashboard)
```
