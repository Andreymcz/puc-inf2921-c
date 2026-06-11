# Check 000035 | REVIEW-staged | 2026-06-11 11:55 UTC | Code Review: plan-000033 like and label traceability

## Scope: plan-000033 changed files (10 files)

## Perspective Evaluation

| Perspective | Status | Summary |
|-------------|--------|---------|
| SEC | Adopted | No injection vectors; user_id flows through Pydantic schema. Advisory: add max_length to `label` field. |
| API | Adopted (after fix) | GET /{id}/likes correct and tested. ValueError → CitizenPostNotFoundError fixed. |
| ARCH | Adopted | Clean layering. label_feedback inner dict is untyped (advisory). |
| TEST | Deferred | Happy paths covered. FakeRepository.get_likes ignores post_id (MEDIUM advisory). Missing unit test for GetPostLikes not-found path. |
| DATA | Adopted (after fix) | app.py vote-state check and dashboard loop both fixed for new dict structure. |

## Issues Found

| # | Severity | Status | Perspective | Description | Location |
|---|----------|--------|-------------|-------------|----------|
| 1 | MEDIUM | Deferred | SEC | `label` field in `LabelFeedbackRequest` has no max_length constraint | `citizen_post_schemas.py:46-49` |
| 2 | HIGH | **FIXED** | API/ARCH | `set_label_feedback` raised ValueError instead of CitizenPostNotFoundError | `sqlalchemy_citizen_post_repository.py:88` |
| 3 | MEDIUM | Deferred | ARCH | `label_feedback: dict[str, dict]` untyped inner dict — introduce `LabelFeedbackEntry` TypedDict | `citizen_post.py:31`, `citizen_post_schemas.py:30` |
| 4 | MEDIUM | Deferred | TEST | No unit test for `GetPostLikes` with a non-existent post | `test_citizen_post_use_cases.py` |
| 5 | MEDIUM | Deferred | TEST | `FakeRepository.get_likes` ignores post_id, breaks multi-post test scenarios | `test_citizen_post_use_cases.py:76` |
| 6 | HIGH | **FIXED** | DATA | `app.py` vote-state check compared dict to `True/False` — broken after structure change | `app.py:127-128` |
| 7 | HIGH | **FIXED** | DATA | Dashboard `feedback_rows` loop treated dict as bool — would raise TypeError | `app.py:186` |

## Generator-Critic Iterations
- Iteration count: 1/2
- Findings per iteration: [3 critical fixed]
- Resolution status: all critical resolved

## Deferred Issues (5 — non-blocking)

Issues 1, 3, 4, 5 are advisory improvements. Consider filing a follow-up plan for:
- Typed `LabelFeedbackEntry` model (#3)
- `FakeRepository.get_likes` post_id filter (#5)
- `GetPostLikes` not-found unit test (#4)
- `label` max_length validation (#1)
