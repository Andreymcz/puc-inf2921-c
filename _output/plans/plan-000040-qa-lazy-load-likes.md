# QA Log — plan-000040 | lazy-load post likes on expander open | 2026-06-11 19:41 UTC

## Brief

get citizen posts/likes only when we open the button ver quem curtiu

## Q&A Session

**Q: What is the current behavior of the "Ver quem curtiu" expander?**

A: In `fala-gavea/app.py:page_posts()` (lines 93–100), for every post with `likes_count > 0`, an `api_get(f"/citizen_posts/{post['id']}/likes")` call is made on every Streamlit rerender — including each time the user clicks the like button, navigates pages, or any other interaction that triggers a rerun. Streamlit does not skip code inside `st.expander(...)` when the expander is closed.

**Q: Why is this a problem?**

A: With 20 posts per page (all seeded with likes), every page rerender fires 20 API calls to `GET /citizen_posts/{id}/likes`. These are serial synchronous calls (httpx, 10s timeout each). Each like button click triggers a rerun → 20 more calls. This is a classic N+1 render pattern.

**Q: What approach does the plan take to fix this?**

A: Session-state caching inside the expander. Replace the eager `api_get` with a "Carregar curtidas" button inside the expander. On first click: fetch from API, cache in `st.session_state[f"likers_{post_id}"]`. On subsequent renders: read from cache, no API call.

**Q: Does this require any backend changes?**

A: No. The `GET /citizen_posts/{id}/likes` endpoint is unchanged. This is a frontend-only optimization.

**Q: What UX tradeoff does this introduce?**

A: The user now sees a "Carregar curtidas" button inside the expander instead of the likers list loading immediately when the expander opens. This is one extra click. The benefit is zero API calls on page load and subsequent reruns. The data persists for the session once loaded.
