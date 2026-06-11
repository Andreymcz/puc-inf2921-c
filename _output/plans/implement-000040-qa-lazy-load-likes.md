# QA Log — implement-000040 | lazy-load post likes on expander open | 2026-06-11 19:50 UTC

## Brief

implement plan-000040

## Implementation Q&A

**Q: What exactly was changed in `fala-gavea/app.py`?**

A: In `page_posts()`, the block inside `if likes > 0:` was modified. Before: the code used `with st.expander("Ver quem curtiu"):` and called `api_get(f"/citizen_posts/{post['id']}/likes")` directly inside the expander body — executing on every page rerender. After: the expander now checks `st.session_state` for a cached result (`cache_key = f"likers_{post['id']}"`). If not cached, shows a "Carregar curtidas" button. Clicking it fetches from API, stores result in session state, and calls `st.rerun()`. If already cached, shows the likers list directly.

**Q: How many lines changed?**

A: 7 lines replaced with 13 lines — net +6 lines in the expander block.

**Q: Was the Python syntax verified?**

A: Yes — `python -m py_compile fala-gavea/app.py` returned exit 0 (no syntax errors).

**Q: Are there any edge cases to watch?**

A: (1) If a post gets new likes after the session loads, the cached list won't reflect them — user must start a new session. Acceptable for a PoC. (2) If the like button is clicked (triggering rerun), the cached likers for that post persist in session state — they will be stale by +1. Minor; acceptable for a PoC.
