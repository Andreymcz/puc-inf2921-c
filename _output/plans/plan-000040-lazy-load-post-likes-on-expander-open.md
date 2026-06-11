# Plan 000040 | feat(fala-gavea) | 2026-06-11 19:35 UTC | lazy-load post likes on expander open | Review: light
plan_format_version: 1

## Brief

> get citizen posts/likes only when we open the button ver quem curtiu

## Problem

In `fala-gavea/app.py:page_posts()` (lines 93–100), the likes list for each post is fetched eagerly on every Streamlit rerender:

```python
if likes > 0:
    with st.expander("Ver quem curtiu"):
        try:
            likes_data = api_get(f"/citizen_posts/{post['id']}/likes")
            ...
```

Streamlit executes all code inside `st.expander(...)` on every rerun — regardless of whether the expander is open or closed. With 20 posts per page and all having likes (seeded dataset), this fires up to 20 `GET /citizen_posts/{id}/likes` API calls on every page render. Each like button press triggers a full rerender, causing another 20 calls.

## Solution

Cache likers in `st.session_state` keyed by post ID. Inside the expander, show a "Carregar" button when data is not yet fetched; show the likers list when it is. This makes the API call happen exactly once per post per session, and only when the user explicitly opens the expander and clicks the button.

## Steps

### Step 1: Add session-state-cached lazy load inside "Ver quem curtiu" expander

In `fala-gavea/app.py`, modify `page_posts()` to replace the eager `api_get` call inside the expander with a button-gated fetch cached in `st.session_state`.

Replace the current block (lines 93–100):

```python
if likes > 0:
    with st.expander("Ver quem curtiu"):
        try:
            likes_data = api_get(f"/citizen_posts/{post['id']}/likes")
            for liker in likes_data.get("likers", []):
                st.caption(f"👤 {citizen_name(liker['user_id'])}")
        except Exception as e:
            st.error(f"Erro ao carregar likes: {e}")
```

With:

```python
if likes > 0:
    cache_key = f"likers_{post['id']}"
    with st.expander("Ver quem curtiu"):
        if cache_key not in st.session_state:
            if st.button("Carregar curtidas", key=f"load_likes_{post['id']}"):
                try:
                    likes_data = api_get(f"/citizen_posts/{post['id']}/likes")
                    st.session_state[cache_key] = likes_data.get("likers", [])
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao carregar likes: {e}")
        else:
            for liker in st.session_state[cache_key]:
                st.caption(f"👤 {citizen_name(liker['user_id'])}")
```

**How it works:**
- On page load: expander renders with a "Carregar curtidas" button — zero API calls.
- On button click: fetches likers once, stores in `st.session_state[f"likers_{post_id}"]`, reruns.
- After fetch: expander shows likers from session state — no further API calls until session resets.
- Pagination navigation (`st.session_state.posts_page` change) triggers a rerun but cached likers are preserved in session state for any previously loaded posts.

- **Files**: `fala-gavea/app.py` (modify)
- **References**: `product-design/project/standards.md § GaveaLab-Specific Standards > Streamlit Conventions`
- **Interface**: N/A
- **Verify**: Start the Streamlit app and the FastAPI backend; open "Postagens"; confirm no network calls to `/citizen_posts/{id}/likes` appear until a "Carregar curtidas" button is clicked; confirm likers appear after clicking; confirm re-navigating pages does not re-fetch for already-loaded posts.
- **Tests**: N/A (UI-only change; no unit-testable logic added)
- [ ] Done

## Review Log

### PERF — Performance

**Adopted.** This plan directly addresses a N+1 render pattern: each page rerender was firing `O(posts_with_likes)` API calls synchronously. Session-state caching eliminates repeat calls within a session. The fix is minimal — one function, one block changed.

### UX — User Experience

**Adopted.** The expander still exists for visual grouping; the "Carregar curtidas" button inside is a standard Streamlit lazy-load pattern. The extra click is a deliberate tradeoff: the user explicitly opts in to loading additional data, which aligns with the intent of the expander ("open to see who liked").

### ARCH — Architecture

**N/A.** Single-file, single-function change. No architectural boundaries affected.
