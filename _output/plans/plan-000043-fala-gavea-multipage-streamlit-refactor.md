# DONE | 2026-06-12 19:10 UTC |
# Plan 000043 | REFACTOR-F frontend | 2026-06-12 11:41 | fala-gavea multipage Streamlit refactor | Review: light
plan_format_version: 1

**User brief:** multipage app with streamlit pages https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app

**Agent interpretation:** Refactor `fala-gavea/app.py` from a 413-line monolith (5 inline page functions + sidebar-radio dispatch) into Streamlit's native multipage structure using `st.navigation()` + `st.Page()`. Each page becomes a standalone module under `fala-gavea/app_pages/`. Shared utilities (API helpers, `citizen_name`, constants) move to `app_pages/shared.py`. The current implicit `USER_ID` global is replaced by `st.session_state.user_id` access in each page. Pattern is consistent with `gavealab-poc/app.py`.

**Files:**
- `fala-gavea/app.py` — rewrite (entry point, navigation setup)
- `fala-gavea/app_pages/__init__.py` — create (package marker)
- `fala-gavea/app_pages/shared.py` — create (API_URL, POSTS_PER_PAGE, citizen_name, api_get, api_post)
- `fala-gavea/app_pages/posts.py` — create (Postagens page)
- `fala-gavea/app_pages/new_post.py` — create (Nova Postagem page)
- `fala-gavea/app_pages/label_feedback.py` — create (Validar Labels page)
- `fala-gavea/app_pages/dashboard.py` — create (Dashboard page)
- `fala-gavea/app_pages/clusters.py` — create (Explorar Clusters page)

---

## Step 1 — Create `app_pages/shared.py` with shared utilities

**Action:** Create `fala-gavea/app_pages/__init__.py` (empty) and `fala-gavea/app_pages/shared.py`.

`shared.py` contains:
- `API_URL: str` — reads `FALA_GAVEA_API_URL` env var, default `http://localhost:8000`
- `POSTS_PER_PAGE: int = 20`
- `_CITIZEN_NAMES: list[str]` — the 30-name list
- `citizen_name(user_id: str) -> str` — MD5-based deterministic name lookup
- `api_get(path: str, **params: object) -> list | dict` — GET wrapper via httpx
- `api_post(path: str, body: dict) -> dict` — POST wrapper via httpx

All imported from `app.py` currently. No logic changes — pure extraction.

```python
# app_pages/shared.py
from __future__ import annotations
import hashlib
import os
import httpx

API_URL: str = os.environ.get("FALA_GAVEA_API_URL", "http://localhost:8000")
POSTS_PER_PAGE: int = 20

_CITIZEN_NAMES: list[str] = [
    "Ana", "Carlos", "Fernanda", "João", "Mariana",
    "Pedro", "Luciana", "Rafael", "Beatriz", "Rodrigo",
    "Camila", "Diego", "Patricia", "André", "Juliana",
    "Marcos", "Vanessa", "Felipe", "Sandra", "Gustavo",
    "Renata", "Bruno", "Tatiana", "Eduardo", "Cristina",
    "Thiago", "Adriana", "Henrique", "Priscila", "Leonardo",
]


def citizen_name(user_id: str) -> str:
    idx = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % len(_CITIZEN_NAMES)
    return _CITIZEN_NAMES[idx]


def api_get(path: str, **params: object) -> list | dict:
    r = httpx.get(f"{API_URL}{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(path: str, body: dict) -> dict:
    r = httpx.post(f"{API_URL}{path}", json=body, timeout=10)
    r.raise_for_status()
    return r.json()
```

---

## Step 2 — Create `app_pages/posts.py`

**Action:** Create `fala-gavea/app_pages/posts.py` with a `render() -> None` function.

Move `page_posts()` body here verbatim, replacing all references to `USER_ID` with `st.session_state.user_id`. Import `citizen_name`, `api_get`, `api_post`, `POSTS_PER_PAGE` from `.shared`.

```python
# app_pages/posts.py
from __future__ import annotations
import streamlit as st
from .shared import citizen_name, api_get, api_post, POSTS_PER_PAGE


def render() -> None:
    st.header("📋 Postagens")
    # ... (page_posts body, USER_ID → st.session_state.user_id)
```

---

## Step 3 — Create `app_pages/new_post.py`

**Action:** Create `fala-gavea/app_pages/new_post.py` with `render() -> None`.

Move `page_new_post()` body here. Replace `USER_ID` with `st.session_state.user_id`. Import `api_post` from `.shared`.

---

## Step 4 — Create `app_pages/label_feedback.py`

**Action:** Create `fala-gavea/app_pages/label_feedback.py` with `render() -> None`.

Move `page_label_feedback()` body here. Replace `USER_ID` with `st.session_state.user_id`. Import `api_get`, `api_post` from `.shared`.

---

## Step 5 — Create `app_pages/dashboard.py`

**Action:** Create `fala-gavea/app_pages/dashboard.py` with `render() -> None`.

Move `page_dashboard()` body here, including the `import pandas as pd` (move to top-level import). Replace `USER_ID` with `st.session_state.user_id`. Import `citizen_name`, `api_get` from `.shared`.

---

## Step 6 — Create `app_pages/clusters.py`

**Action:** Create `fala-gavea/app_pages/clusters.py` with `render() -> None`.

Move `page_clusters()` body here. Import `api_get`, `api_post` from `.shared`; keep imports for `build_cluster_df`, `label_clusters`, `plotly.express`, `pandas`.

Note: `save_btn` is built before the `if run_btn:` block — no change needed, this is correct Streamlit state management.

---

## Step 7 — Rewrite `app.py` as navigation entry point

**Action:** Replace `fala-gavea/app.py` contents with the navigation entry point.

```python
from __future__ import annotations
import uuid
import streamlit as st
from app_pages import posts, new_post, label_feedback, dashboard, clusters

st.set_page_config(page_title="Fala Gavea", page_icon="🗣️", layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

pg = st.navigation(
    [
        st.Page(posts.render, title="Postagens", icon="📋", default=True),
        st.Page(new_post.render, title="Nova Postagem", icon="✍️"),
        st.Page(label_feedback.render, title="Validar Labels", icon="🏷️"),
        st.Page(dashboard.render, title="Dashboard", icon="📊"),
        st.Page(clusters.render, title="Explorar Clusters", icon="🗺️"),
    ]
)

with st.sidebar:
    st.title("🗣️ Fala Gávea")
    st.caption(f"Sessão: `{st.session_state.user_id[:8]}...`")
    st.divider()

pg.run()
```

`st.navigation()` renders its own page list in the sidebar automatically above any custom sidebar content. Sidebar title, session caption, and divider follow below the page list.

---

## Review

**ARCH** — Adopted. Monolith decomposed into single-responsibility modules; shared utilities centralized in `shared.py`; navigation logic isolated in `app.py`. Consistent with `gavealab-poc` structure.

**UX** — Adopted. `st.navigation()` renders a styled page list with icons in the sidebar, replacing the plain `st.radio`. User experience unchanged for all 5 pages; sidebar aesthetics improve.

**DX** — Adopted. Each page is independently readable and editable. Shared code has a single home. New pages require only adding a module + one `st.Page()` entry.

**PERF, SEC, TEST, DB, API, I18N, COMPAT, DATA, A11Y, VIS, RESP, MICRO** — N/A for a pure structural refactor with no behavior change.

---

## Commit message

```
refactor(fala-gavea): migrate app.py to st.navigation() multipage structure

Split 413-line monolith into app_pages/ package (shared.py + 5 page modules).
Each page exports render(); app.py now owns only page config and st.navigation()
dispatch. Consistent with gavealab-poc multipage pattern.
```
