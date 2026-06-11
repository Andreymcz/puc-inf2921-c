# Progress -- Plan 000033

Append-only cross-iteration learnings. Each subagent reads this file at the start and appends findings at the end.

## Codebase Patterns
<!-- Subagents consolidate reusable patterns here -->

## Iteration Log

### Step 1 — 2026-06-11 — SUCCESS

**Changes made:**
- `fala-gavea/src/fala_gavea/domain/entities/citizen_post.py`: Added `LikeRecord` dataclass with `user_id: str` and `created_at: datetime` fields. Updated `CitizenPost.label_feedback` type from `dict[str, bool]` to `dict[str, dict]`.
- `fala-gavea/src/fala_gavea/domain/repositories/citizen_post_repository.py`: Imported `LikeRecord`; added `get_likes(post_id: str) -> list[LikeRecord]` as abstract method.
- `fala-gavea/src/fala_gavea/infrastructure/repositories/sqlalchemy_citizen_post_repository.py`: Added `get_likes` concrete implementation (queries `LikeModel` by `post_id`, returns `list[LikeRecord]` using `cast()` for SQLAlchemy Column type safety). Added `LikeRecord` import.

**Pyright result:** 19 errors (all pre-existing SQLAlchemy untyped Column issues in infrastructure layer, 1 fewer than baseline of 20). No new errors introduced.

**Commit:** `81e52f6` — `plan-000033 step 1: add LikeRecord dataclass and get_likes abstract method`

**Note:** SQLAlchemy models use legacy untyped `Column` (not `Mapped[]`), so infrastructure-layer type errors are pre-existing. The `get_likes` implementation uses `cast()` to avoid adding new errors. Later plan steps should migrate to `Mapped[]` typed columns to clear these 19 pre-existing errors.

### Step 2 — 2026-06-11 — SUCCESS

**Changes made:**
- `fala-gavea/src/fala_gavea/domain/repositories/citizen_post_repository.py`: Added missing abstract methods `add_like`, `remove_like`, `has_liked`; added `set_label_feedback(post_id, label, approved, user_id)` as abstract method with new `user_id` parameter.
- `fala-gavea/src/fala_gavea/infrastructure/repositories/sqlalchemy_citizen_post_repository.py`: Updated `set_label_feedback` signature to include `user_id: str`; stores `{"approved": approved, "user_id": user_id}` dict instead of bare `bool`.
- `fala-gavea/src/fala_gavea/application/use_cases/add_label_feedback.py`: Added `user_id: str` to `AddLabelFeedbackInput`; use case passes it to `repo.set_label_feedback`.
- `fala-gavea/src/fala_gavea/presentation/api/routers/citizen_posts.py`: Forwards `body.user_id` to `AddLabelFeedbackInput`.
- `fala-gavea/src/fala_gavea/presentation/schemas/citizen_post_schemas.py`: `CitizenPostResponse.label_feedback` type updated from `dict[str, bool]` to `dict[str, dict]`.
- `fala-gavea/tests/unit/application/test_citizen_post_use_cases.py`: `FakeRepository` updated — added `get_likes`, updated `set_label_feedback` to store dict and accept `user_id`, added `_like_records` tracking; updated existing label feedback test; added `test_set_label_feedback_stores_user_id` and `test_get_likes_returns_likers`.
- `fala-gavea/tests/integration/api/test_citizen_posts_api.py`: `test_add_label_feedback` assertion updated to check nested dict fields.

**Tests:** 26 passed (was 23 before — 3 new tests added).

**Pyright result:** 15 errors (all pre-existing SQLAlchemy untyped Column issues — fewer than Step 1 baseline of 19). No new errors introduced.

**Commit:** `07f8a90` — `plan-000033 step 2: update set_label_feedback to store user_id`

**Note:** `dev` extras were not installed in the venv; required `uv sync --extra dev` before tests could run. The `pytest` binary is now present. The `FakeRepository.get_likes` returns all like records (not filtered by post_id) — acceptable for unit test scope since the fake is post-scoped per test.

### Step 3 — 2026-06-11 — SUCCESS

**Changes made:**
- `fala-gavea/src/fala_gavea/application/use_cases/get_post_likes.py`: Created new `GetPostLikesInput` dataclass and `GetPostLikes` use case class that delegates to `repo.get_likes(inp.post_id)`.
- `fala-gavea/tests/unit/application/test_citizen_post_use_cases.py`: Added import for `GetPostLikes, GetPostLikesInput`; added `test_get_post_likes_returns_records` unit test that creates a post, toggles likes for two users, then verifies the use case returns 2 `LikeRecord` objects with correct `user_id` values and non-None `created_at`.

**Tests:** 27 passed (was 26 before — 1 new test added).

**Pyright result:** 15 errors (all pre-existing SQLAlchemy untyped Column issues — same count as Step 2). No new errors introduced.

**Commit:** `2c08090` — `plan-000033 step 3: add GetPostLikes use case`

### Step 4 — 2026-06-11 — SUCCESS

**Changes made:**
- `fala-gavea/src/fala_gavea/presentation/schemas/citizen_post_schemas.py`: Added `LikeRecordResponse(BaseModel)` with `user_id: str` and `created_at: datetime`; added `PostLikesResponse(BaseModel)` with `post_id: str` and `likers: list[LikeRecordResponse]`.
- `fala-gavea/src/fala_gavea/presentation/api/routers/citizen_posts.py`: Imported `GetPostLikes`, `GetPostLikesInput`, `LikeRecordResponse`, `PostLikesResponse`; added `GET /{id}/likes` endpoint returning `PostLikesResponse` with 404 on `CitizenPostNotFoundError`.
- `fala-gavea/src/fala_gavea/application/use_cases/get_post_likes.py`: Updated `execute` to call `find_by_id` and raise `CitizenPostNotFoundError` if the post doesn't exist, enabling proper 404 responses.
- `fala-gavea/tests/integration/api/test_citizen_posts_api.py`: Added `test_get_post_likes_endpoint` (empty list, then one like with user_id and created_at) and `test_get_post_likes_not_found_returns_404`.

**Tests:** 29 passed (was 27 before — 2 new integration tests added).

**Pyright result:** 15 errors (all pre-existing SQLAlchemy untyped Column issues — same count as Step 3). No new errors introduced.

**Commit:** `1d731bc` — `plan-000033 step 4: add GET /citizen_posts/{id}/likes endpoint and schemas`

**Note:** The `GetPostLikes` use case now validates post existence via `find_by_id` before querying likes, making the 404 behavior consistent with other endpoints.

### Step 5 — 2026-06-11 — SUCCESS

**Changes made:**
- `fala-gavea/app.py`: In `page_posts`, added a `st.expander("Ver quem curtiu")` inside the like button column that only renders when `likes_count > 0`. On expansion, calls `api_get(f"/citizen_posts/{post['id']}/likes")` and displays each liker's truncated `user_id`.
- `fala-gavea/app.py`: In `page_dashboard`, added "Rastreabilidade de likes" subsection with a "Carregar rastreabilidade" button that bulk-fetches likes for all posts with `likes_count > 0` and shows a table with `post_id[:8]`, `texto[:40]`, and joined liker user IDs.
- `fala-gavea/app.py`: In `page_dashboard`, added "Rastreabilidade de labels" subsection that reads `label_feedback` from already-loaded posts and displays a table with columns `label`, `aprovado`, `usuario` — handles the new `{"approved": bool, "user_id": str}` dict structure (not the old bare `bool`).

**Syntax check:** `ast.parse` passed cleanly (UTF-8).

**Commit:** `ba04750` — `plan-000033 step 5: add like and label traceability to Streamlit UI`

**Note:** Like traceability uses an on-demand button to avoid N+1 API calls on page render. Label traceability reads from already-loaded post data (no extra API calls needed). Both handle empty/missing data gracefully with `st.info(...)` fallbacks.
