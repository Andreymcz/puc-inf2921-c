# DONE | 2026-06-11 17:12 UTC | Plan 000036 | FIX-F fala-gavea | 2026-06-11 16:48 | posts pagination, citizen names, encoding fix | Review: light
plan_format_version: 1

## Brief

**User:** add paginaçao das postagens, inventar nomes melhores para os cidadaos, fix problema com encoding: "A situaÃ§Ã£o da saÃºde aqui tÃ¡ precÃ¡ria demais. "

**Interpretation:** Three improvements to the Fala Gávea Streamlit app and seed script:

1. **Encoding fix** — `seed_db.py` opens `sample-gavealab-1000.csv` with `encoding="latin-1"` but the file is UTF-8 (`file` command confirms UTF-8 Unicode text). This produces the classic Mojibake (e.g., `situação` → `situaÃ§Ã£o`). Fix: change to `encoding="utf-8"`.

2. **Citizen names** — Posts and likes currently display raw UUIDs truncated to 8 chars (`author_id[:8]...`). Replace with deterministic human-readable Brazilian first names derived from a hash of the UUID — no data change, purely presentational.

3. **Posts pagination** — `page_posts()` fetches up to 100 posts at once with no navigation. The backend already accepts `limit` + `offset` on `GET /citizen_posts/`. Add Streamlit-side page state (`st.session_state.posts_page`) and prev/next controls fetching 20 posts per page.

---

## Files

| File | Change |
|------|--------|
| `fala-gavea/scripts/seed_db.py` | Fix `encoding="latin-1"` → `"utf-8"` |
| `fala-gavea/app.py` | Add `citizen_name()`, add `POSTS_PER_PAGE`, paginate `page_posts()`, replace UUID display in posts + likes + dashboard |

---

## Steps

### Step 1 — Fix CSV encoding in seed_db.py

**File:** `fala-gavea/scripts/seed_db.py`

In `load_csv()`, change:
```python
with open(DATA_FILE, encoding="latin-1") as f:
```
to:
```python
with open(DATA_FILE, encoding="utf-8") as f:
```

The CSV is UTF-8 (confirmed by `file` command). The latin-1 encoding causes multi-byte UTF-8 sequences to be decoded as individual latin-1 characters, producing Mojibake. No other changes needed in this file.

**Note:** The existing database (`app.db`) was seeded with the broken encoding. After applying this fix, a fresh re-seed is needed to get clean text. This is a data migration concern outside the plan scope — the fix prevents future corruption.

---

### Step 2 — Add citizen_name() to app.py

**File:** `fala-gavea/app.py`

Add `import hashlib` to the existing imports.

Add the following constant and function after the `API_URL` / `USER_ID` setup block and before the `# -- helpers --` section:

```python
_CITIZEN_NAMES: list[str] = [
    "Ana", "Carlos", "Fernanda", "João", "Mariana",
    "Pedro", "Luciana", "Rafael", "Beatriz", "Rodrigo",
    "Camila", "Diego", "Patricia", "André", "Juliana",
    "Marcos", "Vanessa", "Felipe", "Sandra", "Gustavo",
    "Renata", "Bruno", "Tatiana", "Eduardo", "Cristina",
    "Thiago", "Adriana", "Henrique", "Priscila", "Leonardo",
]

def citizen_name(user_id: str) -> str:
    """Deterministic human-readable name from a UUID."""
    idx = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % len(_CITIZEN_NAMES)
    return _CITIZEN_NAMES[idx]
```

The list has 30 common Brazilian first names. `hashlib.md5` is used for speed only — no security requirement here. The mapping is stable: the same UUID always produces the same name.

---

### Step 3 — Replace UUID display with citizen_name()

**File:** `fala-gavea/app.py`

Four substitutions:

**3a. Post card caption** (in `page_posts()`):
```python
# before
st.caption(f"👤 {post['author_id'][:8]}...  ·  {post['created_at'][:10]}")
# after
st.caption(f"👤 {citizen_name(post['author_id'])}  ·  {post['created_at'][:10]}")
```

**3b. Likes expander** (in `page_posts()`):
```python
# before
st.caption(f"👤 {liker['user_id'][:8]}...")
# after
st.caption(f"👤 {citizen_name(liker['user_id'])}")
```

**3c. Dashboard "Rastreabilidade de likes"** — the `curtidores` field in `likes_rows`:
```python
# before
"curtidores": ", ".join(u[:8] for u in likers),
# after
"curtidores": ", ".join(citizen_name(u) for u in likers),
```

**3d. Dashboard "Rastreabilidade de labels"**:
```python
# before
"usuario": str(info.get("user_id", ""))[:8],
# after
"usuario": citizen_name(str(info.get("user_id", "") or "")),
```

For 3d, guard against empty string: `citizen_name` will be called with `""` when `user_id` is absent — `hashlib.md5(b"")` is deterministic, so it returns a valid name consistently. This is acceptable.

---

### Step 4 — Add pagination to page_posts()

**File:** `fala-gavea/app.py`

**4a.** Add page-size constant after `API_URL`:
```python
POSTS_PER_PAGE = 20
```

**4b.** Replace the entire `page_posts()` function body with a paginated version:

```python
def page_posts() -> None:
    st.header("📋 Postagens")

    if "posts_page" not in st.session_state:
        st.session_state.posts_page = 0

    page: int = st.session_state.posts_page
    offset = page * POSTS_PER_PAGE

    try:
        posts = api_get("/citizen_posts/", limit=POSTS_PER_PAGE, offset=offset)
    except Exception as e:
        st.error(f"Erro ao carregar postagens: {e}")
        return

    if not posts and page == 0:
        st.info("Nenhuma postagem ainda. Crie a primeira!")
        return

    for post in posts:
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{post['territory_name']}** · _{post['territory_level']}_")
                st.write(post["text"])
                if post.get("ai_labels"):
                    st.caption("Labels: " + ", ".join(post["ai_labels"]))
                st.caption(f"👤 {citizen_name(post['author_id'])}  ·  {post['created_at'][:10]}")
            with col2:
                likes = post.get("likes_count", 0)
                if st.button(f"❤️ {likes}", key=f"like_{post['id']}"):
                    try:
                        api_post(f"/citizen_posts/{post['id']}/likes", {"user_id": USER_ID})
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                if likes > 0:
                    with st.expander("Ver quem curtiu"):
                        try:
                            likes_data = api_get(f"/citizen_posts/{post['id']}/likes")
                            for liker in likes_data.get("likers", []):
                                st.caption(f"👤 {citizen_name(liker['user_id'])}")
                        except Exception as e:
                            st.error(f"Erro ao carregar likes: {e}")

    # pagination controls
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    with col_prev:
        if page > 0:
            if st.button("← Anterior"):
                st.session_state.posts_page -= 1
                st.rerun()
    with col_info:
        start = offset + 1
        end = offset + len(posts)
        st.caption(f"Postagens {start}–{end} · página {page + 1}")
    with col_next:
        if len(posts) == POSTS_PER_PAGE:
            if st.button("Próxima →"):
                st.session_state.posts_page += 1
                st.rerun()
```

The "Próxima →" button is shown only when the current page returned exactly `POSTS_PER_PAGE` results, meaning there may be more. When a page returns fewer than `POSTS_PER_PAGE` items it is the last page.

---

## Review log (light)

| Perspective | Status | Note |
|-------------|--------|------|
| Correctness | Adopted | Encoding fix is the direct cause of the Mojibake; latin-1 → utf-8 resolves it. citizen_name uses stable MD5 hash. Pagination uses backend offset which is already tested. |
| Security | N/A | No auth changes; no new external inputs; hashlib.md5 used for determinism only, not security. |
| UX / communicability | Adopted | Brazilian first names are immediately legible; pagination avoids loading 1000 posts at once. |
| Performance | Adopted | Fetching 20 posts per page instead of 100–1500 reduces API response time and DOM size. |

---

## Docs

No documentation update required — internal app changes only.

---

## Implementation Summary

**Completed:** 2026-06-11 17:12 UTC | **Steps:** 4/4 | **Files changed:** 2

### Changes applied

| File | Change |
|------|--------|
| `fala-gavea/scripts/seed_db.py` | `encoding="latin-1"` → `encoding="utf-8"` in `load_csv()` |
| `fala-gavea/app.py` | Added `import hashlib`, `POSTS_PER_PAGE = 20`, `_CITIZEN_NAMES` list, `citizen_name()` function |
| `fala-gavea/app.py` | Replaced all `user_id[:8]...` displays with `citizen_name()` (posts captions, likes expander, dashboard likes traceability, dashboard label traceability) |
| `fala-gavea/app.py` | Replaced `page_posts()` with paginated version using `st.session_state.posts_page`, fetches 20 posts per page, prev/next controls |

### Notes

- Existing `app.db` was seeded with broken latin-1 encoding — a fresh `seed_db.py` run is needed to get clean UTF-8 text in the database.
- `citizen_name("")` is safe: `hashlib.md5(b"")` is deterministic and returns a valid name for absent `user_id` values.
