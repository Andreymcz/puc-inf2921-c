# Plan 000033 | FEATURE-B | 2026-06-11 11:18 | fala-gavea: like and label traceability
plan_format_version: 1
Review: standard

## Brief

rastrabilidade de likes e labels. quero saber quem foi que deu like nos posts

## Agent Interpretation

Expose WHO liked each post and WHO gave label feedback. The `LikeModel` table already stores `user_id + post_id + created_at`, so like traceability needs only a new repository method and API endpoint. Label traceability requires storing the `user_id` alongside the `approved` flag in the `label_feedback` JSON column (currently just `{label: bool}`). Both surfaces are then shown in the Streamlit dashboard.

## Context

### What already exists

| Component | Location | Notes |
|-----------|----------|-------|
| `LikeModel` table | `fala-gavea/src/fala_gavea/infrastructure/database/models.py` | PK: `(user_id, post_id)`, has `created_at` |
| `has_liked`, `add_like`, `remove_like` | `SQLAlchemyCitizenPostRepository` | No `get_likes` method yet |
| `CitizenPostRepository` (abstract) | `domain/repositories/citizen_post_repository.py` | Missing `get_likes` abstract method |
| `label_feedback` JSON column | `CitizenPostModel` | Stores `{label: bool}` -- no user attribution |
| `LabelFeedbackRequest.user_id` | `presentation/schemas/citizen_post_schemas.py` | Arrives at API but is discarded by `set_label_feedback` |
| `GET /citizen_posts/{id}/likes` | -- | Does not exist |

### What must change

1. **Domain**: add `get_likes(post_id) -> list[LikeRecord]` to the repository interface. Add `LikeRecord` dataclass.
2. **Domain**: change `CitizenPost.label_feedback` type from `dict[str, bool]` to `dict[str, dict]` where each value is `{"approved": bool, "user_id": str}`.
3. **Infrastructure**: implement `get_likes` in `SQLAlchemyCitizenPostRepository`. Update `set_label_feedback` to persist `{"approved": ..., "user_id": ...}`.
4. **Application**: add `GetPostLikes` use case. Update `AddLabelFeedback` to pass `user_id` through.
5. **Presentation/API**: add `LikeRecord` response schema; add `GET /citizen_posts/{id}/likes` endpoint. Update `AddLabelFeedbackInput` to carry `user_id`.
6. **Frontend**: update dashboard to show top likers per post and label feedback attribution in `app.py`.

### Schema note

`label_feedback` is a JSON column -- no SQL migration is needed to change its shape. Existing fake-data rows with the old `{label: bool}` structure will be unreadable by the new code. Resetting the seed dataset (plan-000032) before or after this plan resolves that.

---

## Steps

### Step 1: Add `LikeRecord` dataclass and `get_likes` abstract method to domain layer

Add a `LikeRecord` dataclass to `citizen_post.py` with fields `user_id: str` and `created_at: datetime`. Add `get_likes(post_id: str) -> list[LikeRecord]` as an abstract method on `CitizenPostRepository`. Update `CitizenPost.label_feedback` type annotation from `dict[str, bool]` to `dict[str, dict]`.

The `LikeRecord` dataclass:
```python
@dataclass
class LikeRecord:
    user_id: str
    created_at: datetime
```

The domain entity type change is annotation-only -- no logic in the entity changes; the business rule (label -> feedback value) is enforced in the repository and use case.

- **Files**: `fala-gavea/src/fala_gavea/domain/entities/citizen_post.py` (modify), `fala-gavea/src/fala_gavea/domain/repositories/citizen_post_repository.py` (modify)
- **References**: `product-design/project/standards.md § Backend`
- **Interface**: exports `LikeRecord` dataclass with `user_id: str, created_at: datetime`; `CitizenPostRepository.get_likes(post_id: str) -> list[LikeRecord]` abstract method
- **Verify**: `uv run pyright src/` passes with no new errors
- **Tests**: N/A (domain interface -- covered by integration tests in Step 4)
- [ ] Done

### Step 2: Implement `get_likes` and update `set_label_feedback` in the SQLAlchemy repository

In `SQLAlchemyCitizenPostRepository`:

1. Add `get_likes(post_id: str) -> list[LikeRecord]`:
   ```python
   def get_likes(self, post_id: str) -> list[LikeRecord]:
       rows = (
           self._session.query(LikeModel)
           .filter(LikeModel.post_id == post_id)
           .order_by(LikeModel.created_at.desc())
           .all()
       )
       return [LikeRecord(user_id=r.user_id, created_at=r.created_at) for r in rows]
   ```

2. Update `set_label_feedback` to accept and persist `user_id`:
   - Change signature to `set_label_feedback(self, post_id: str, label: str, approved: bool, user_id: str) -> CitizenPost`
   - Store `{"approved": approved, "user_id": user_id}` instead of `approved` directly

- **Files**: `fala-gavea/src/fala_gavea/infrastructure/repositories/sqlalchemy_citizen_post_repository.py` (modify)
- **References**: `product-design/project/standards.md § Backend`
- **Depends on**: Step 1
- **Interface**: `get_likes(post_id) -> list[LikeRecord]`; `set_label_feedback(post_id, label, approved, user_id) -> CitizenPost`
- **Verify**: `uv run pyright src/` passes; existing unit tests still pass
- **Tests**: Add `test_get_likes_returns_likers` and `test_set_label_feedback_stores_user_id` to `tests/unit/application/test_citizen_post_use_cases.py` or a new `tests/integration/api/test_likes_api.py`
- [ ] Done

### Step 3: Add `GetPostLikes` use case and update `AddLabelFeedback`

Add `fala-gavea/src/fala_gavea/application/use_cases/get_post_likes.py`:
```python
@dataclass
class GetPostLikesInput:
    post_id: str

class GetPostLikes:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: GetPostLikesInput) -> list[LikeRecord]:
        return self._repo.get_likes(inp.post_id)
```

Update `AddLabelFeedbackInput` in `add_label_feedback.py` to include `user_id: str`, and pass it to `repo.set_label_feedback(...)`.

- **Files**: `fala-gavea/src/fala_gavea/application/use_cases/get_post_likes.py` (create), `fala-gavea/src/fala_gavea/application/use_cases/add_label_feedback.py` (modify)
- **References**: `product-design/project/standards.md § Backend`
- **Depends on**: Step 2
- **Interface**: exports `GetPostLikes` with `execute(inp: GetPostLikesInput) -> list[LikeRecord]`; `AddLabelFeedbackInput.user_id: str`
- **Verify**: `uv run pyright src/` passes
- **Tests**: Add `test_get_post_likes_returns_records` unit test; update existing `AddLabelFeedback` tests to pass `user_id`
- [ ] Done

### Step 4: Add API schemas and `GET /citizen_posts/{id}/likes` endpoint

In `presentation/schemas/citizen_post_schemas.py`:
- Add `LikeRecordResponse(BaseModel)` with `user_id: str` and `created_at: datetime`
- Add `PostLikesResponse(BaseModel)` with `post_id: str` and `likers: list[LikeRecordResponse]`

In `presentation/api/routers/citizen_posts.py`:
- Add `GET /citizen_posts/{id}/likes` endpoint that calls `GetPostLikes(repo).execute(...)` and returns `PostLikesResponse`
- Update `toggle_like` route's `LikeRequest` import is unchanged (no impact)
- Update `add_label_feedback` router handler to forward `body.user_id` to `AddLabelFeedbackInput`

```python
@router.get("/{id}/likes", response_model=PostLikesResponse)
def get_post_likes(
    id: str,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> PostLikesResponse:
    try:
        records = GetPostLikes(repo).execute(GetPostLikesInput(post_id=id))
        return PostLikesResponse(
            post_id=id,
            likers=[LikeRecordResponse(user_id=r.user_id, created_at=r.created_at) for r in records],
        )
    except CitizenPostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
```

- **Files**: `fala-gavea/src/fala_gavea/presentation/schemas/citizen_post_schemas.py` (modify), `fala-gavea/src/fala_gavea/presentation/api/routers/citizen_posts.py` (modify)
- **References**: `product-design/project/standards.md § Backend`
- **Depends on**: Step 3
- **Interface**: `GET /citizen_posts/{id}/likes` returns `PostLikesResponse`; `add_label_feedback` now uses `body.user_id`
- **Verify**: `uv run pytest tests/` passes; `GET /citizen_posts/{id}/likes` returns 200 with likers list
- **Tests**: Add `test_get_post_likes_endpoint` to `tests/integration/api/test_citizen_posts_api.py`; update `test_add_label_feedback_endpoint` to confirm user_id stored
- **Docs**: Update `product-design/project/product-design-as-coded.md` § 0b with new endpoint and schema change
- [ ] Done

### Step 5: Update Streamlit frontend to show like and label traceability

In `fala-gavea/app.py`:

**Posts page (`page_posts`)**: under each post's like button, when expanded (or inline), show "Curtido por: user1, user2, ..." using `api_get(f"/citizen_posts/{post['id']}/likes")`. Use `st.expander("Ver quem curtiu")` to avoid cluttering the list. Only show when `likes_count > 0`.

**Dashboard page (`page_dashboard`)**:
- Add a new subsection "Rastreabilidade de likes" with a table of all posts and their likers (post_id[:8], text[:40], likers list).
- Add a "Rastreabilidade de labels" subsection showing a table with columns: `label`, `aprovado`, `usuario`, computed from the new `label_feedback` structure `{label: {"approved": bool, "user_id": str}}`.

Note: the dashboard already loads posts via `api_get("/citizen_posts/", limit=500)`. For like traceability, a separate request per post is expensive. Instead, add a "Carregar rastreabilidade" button that bulk-fetches likes for all posts on demand.

- **Files**: `fala-gavea/app.py` (modify)
- **References**: `product-design/project/standards.md § GaveaLab-Specific Standards`
- **Depends on**: Step 4
- **Interface**: N/A
- **Verify**: Streamlit app starts without errors; posts page shows "Ver quem curtiu" expander; dashboard shows both traceability tables
- **Tests**: N/A (UI-only, manual verification)
- **Docs**: Update `product-design/project/product-design-as-coded.md` § 0b with frontend changes
- [ ] Done

---

## Review

### Perspectives evaluated

| Tag | Finding | Status |
|-----|---------|--------|
| API | `GET /{id}/likes` follows REST collection pattern (resource/sub-resource). No conflicts with existing routes. | Adopted |
| DB | `label_feedback` JSON column change: no SQL migration, but existing rows with old `{label: bool}` structure will parse incorrectly. Seed data reset (plan-000032) recommended before or after this plan. | Adopted -- note in Step 2 |
| DATA | `user_id` in label feedback is a UUID generated client-side -- same trust level as current like attribution. No PII risk beyond what already exists. | Adopted |
| ARCH | New use case `GetPostLikes` follows existing pattern (dataclass input, single `execute` method). `AddLabelFeedback` signature change is backward-incompatible -- all callers are internal, so this is safe. | Adopted |
| SEC | `GET /{id}/likes` is read-only; no new write surface. `user_id` is not validated beyond being a non-empty string (consistent with existing likes). | Adopted |
| PERF | Dashboard "Carregar rastreabilidade" button avoids N+1 per-post likes fetch on page load. | Adopted |
| TEST | Unit tests for new use case; integration tests for new endpoint and updated label feedback endpoint. | Adopted |
| UX | `st.expander("Ver quem curtiu")` keeps posts page clean. Dashboard traceability section is on-demand. | Adopted |

---

## Files Summary

| File | Action |
|------|--------|
| `fala-gavea/src/fala_gavea/domain/entities/citizen_post.py` | modify -- add `LikeRecord`, update `label_feedback` type |
| `fala-gavea/src/fala_gavea/domain/repositories/citizen_post_repository.py` | modify -- add `get_likes` abstract method |
| `fala-gavea/src/fala_gavea/infrastructure/repositories/sqlalchemy_citizen_post_repository.py` | modify -- implement `get_likes`, update `set_label_feedback` |
| `fala-gavea/src/fala_gavea/application/use_cases/get_post_likes.py` | create |
| `fala-gavea/src/fala_gavea/application/use_cases/add_label_feedback.py` | modify -- add `user_id` to input |
| `fala-gavea/src/fala_gavea/presentation/schemas/citizen_post_schemas.py` | modify -- add `LikeRecordResponse`, `PostLikesResponse` |
| `fala-gavea/src/fala_gavea/presentation/api/routers/citizen_posts.py` | modify -- add GET likes endpoint, forward user_id in label feedback |
| `fala-gavea/app.py` | modify -- posts page expander + dashboard traceability sections |
| `tests/integration/api/test_citizen_posts_api.py` | modify -- add likes endpoint tests |
| `tests/unit/application/test_citizen_post_use_cases.py` | modify -- add GetPostLikes tests |

---

## Commit message

```
feat(fala-gavea): add like and label feedback traceability

Expose GET /citizen_posts/{id}/likes (who liked each post).
Store user_id in label_feedback JSON alongside the approval flag.
Dashboard shows on-demand traceability tables for both.
```
