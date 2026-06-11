# Plan 000029 | FEATURE-B | 2026-06-11 03:42 UTC | fala-gavea: backend likes e label_feedback endpoints | Review: light
plan_format_version: 1

source: roadmap-000028 -- W0-1

## User Brief

Adicionar endpoints ao backend FastAPI para: toggle de like por usuário em um post (one-like-per-user), e registro de feedback de label (thumbs up/down). O `likes_count` passa a ser derivado da tabela de likes. O `label_feedback` no post é um dict `{label: bool}` já existente na entidade, só precisa de um endpoint dedicado.

## Agent Interpretation

A entidade `CitizenPost` já tem `likes_count: int` e `label_feedback: dict[str, bool]`. O modelo SQLAlchemy (`CitizenPostModel`) armazena esses campos. Para suportar one-like-per-user precisamos:

1. **Novo modelo `LikeModel`** — tabela `likes` com `(user_id, post_id)` como PK composta. `likes_count` no post será um count derivado (atualizado a cada toggle).
2. **Novos use cases**: `ToggleLike`, `AddLabelFeedback`
3. **Novos endpoints no router**: `POST /citizen_posts/{id}/likes`, `DELETE /citizen_posts/{id}/likes`, `POST /citizen_posts/{id}/label_feedback`
4. **Novos schemas Pydantic**: `LikeRequest`, `LikeResponse`, `LabelFeedbackRequest`
5. **Atualizar `pyproject.toml`** para adicionar `streamlit>=1.35` e `httpx>=0.27` (usados pelo frontend no plan-000030)

## Files

- `fala-gavea/src/fala_gavea/infrastructure/database/models.py` — adicionar `LikeModel`
- `fala-gavea/src/fala_gavea/domain/repositories/citizen_post_repository.py` — adicionar métodos abstratos `add_like`, `remove_like`, `has_liked`
- `fala-gavea/src/fala_gavea/infrastructure/repositories/sqlalchemy_citizen_post_repository.py` — implementar `add_like`, `remove_like`, `has_liked`
- `fala-gavea/src/fala_gavea/application/use_cases/toggle_like.py` — criar
- `fala-gavea/src/fala_gavea/application/use_cases/add_label_feedback.py` — criar
- `fala-gavea/src/fala_gavea/presentation/schemas/citizen_post_schemas.py` — adicionar `LikeRequest`, `LikeResponse`, `LabelFeedbackRequest`
- `fala-gavea/src/fala_gavea/presentation/api/routers/citizen_posts.py` — adicionar 3 endpoints
- `fala-gavea/pyproject.toml` — adicionar `streamlit>=1.35`, `httpx>=0.27`
- `fala-gavea/tests/unit/application/test_citizen_post_use_cases.py` — testes para ToggleLike e AddLabelFeedback
- `fala-gavea/tests/integration/api/test_citizen_posts_api.py` — testes de integração para os novos endpoints

## Steps

### Step 1 — Novo modelo LikeModel e atualização de pyproject.toml

**`fala-gavea/src/fala_gavea/infrastructure/database/models.py`** — adicionar `LikeModel`:

```python
from sqlalchemy import JSON, Column, DateTime, Enum as SAEnum, Integer, String, ForeignKey, UniqueConstraint
from .session import Base
from ...domain.entities.citizen_post import TerritoryLevel


class CitizenPostModel(Base):
    __tablename__ = "citizen_posts"
    id = Column(String, primary_key=True)
    text = Column(String, nullable=False)
    territory_level = Column(SAEnum(TerritoryLevel), nullable=False)
    territory_name = Column(String, nullable=False)
    author_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    ai_labels = Column(JSON, nullable=False, default=list)
    label_feedback = Column(JSON, nullable=False, default=dict)
    likes_count = Column(Integer, nullable=False, default=0)


class LikeModel(Base):
    __tablename__ = "likes"
    user_id = Column(String, nullable=False, primary_key=True)
    post_id = Column(String, ForeignKey("citizen_posts.id"), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False)
```

`likes_count` em `CitizenPostModel` continua sendo gerenciado explicitamente (incrementado/decrementado nos use cases) para evitar N+1 queries no list.

**`fala-gavea/pyproject.toml`** — adicionar dependências do frontend:

```toml
dependencies = [
    "fastapi[standard]>=0.115",
    "sqlalchemy>=2.0",
    "pydantic>=2.0",
    "uvicorn[standard]>=0.30",
    "streamlit>=1.35",
    "httpx>=0.27",
]
```

- [ ] Done

**Tests:** N/A (schema only)
**Verify:** `uv sync` no diretório `fala-gavea/` completa sem erros.

---

### Step 2 — Repositório: métodos abstratos e implementação

**`fala-gavea/src/fala_gavea/domain/repositories/citizen_post_repository.py`** — adicionar:

```python
from abc import ABC, abstractmethod
from ..entities.citizen_post import CitizenPost


class CitizenPostRepository(ABC):
    @abstractmethod
    def save(self, entity: CitizenPost) -> CitizenPost: ...

    @abstractmethod
    def find_by_id(self, id: str) -> CitizenPost | None: ...

    @abstractmethod
    def find_all(self, limit: int = 50, offset: int = 0) -> list[CitizenPost]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

    @abstractmethod
    def add_like(self, post_id: str, user_id: str) -> CitizenPost: ...

    @abstractmethod
    def remove_like(self, post_id: str, user_id: str) -> CitizenPost: ...

    @abstractmethod
    def has_liked(self, post_id: str, user_id: str) -> bool: ...

    @abstractmethod
    def set_label_feedback(self, post_id: str, label: str, approved: bool) -> CitizenPost: ...
```

**`fala-gavea/src/fala_gavea/infrastructure/repositories/sqlalchemy_citizen_post_repository.py`** — implementar os 4 novos métodos:

```python
from datetime import UTC, datetime
from ..database.models import LikeModel

def add_like(self, post_id: str, user_id: str) -> CitizenPost:
    post = self._session.get(CitizenPostModel, post_id)
    if post is None:
        raise ValueError(f"Post {post_id} not found")
    existing = self._session.get(LikeModel, (user_id, post_id))
    if existing:
        return self._to_entity(post)
    like = LikeModel(user_id=user_id, post_id=post_id, created_at=datetime.now(UTC))
    post.likes_count = (post.likes_count or 0) + 1
    self._session.add(like)
    self._session.commit()
    self._session.refresh(post)
    return self._to_entity(post)

def remove_like(self, post_id: str, user_id: str) -> CitizenPost:
    post = self._session.get(CitizenPostModel, post_id)
    if post is None:
        raise ValueError(f"Post {post_id} not found")
    like = self._session.get(LikeModel, (user_id, post_id))
    if like:
        self._session.delete(like)
        post.likes_count = max(0, (post.likes_count or 0) - 1)
        self._session.commit()
        self._session.refresh(post)
    return self._to_entity(post)

def has_liked(self, post_id: str, user_id: str) -> bool:
    return self._session.get(LikeModel, (user_id, post_id)) is not None

def set_label_feedback(self, post_id: str, label: str, approved: bool) -> CitizenPost:
    post = self._session.get(CitizenPostModel, post_id)
    if post is None:
        raise ValueError(f"Post {post_id} not found")
    feedback = dict(post.label_feedback or {})
    feedback[label] = approved
    post.label_feedback = feedback
    self._session.commit()
    self._session.refresh(post)
    return self._to_entity(post)
```

- [ ] Done

**Tests:** N/A (implementação coberta pelos testes do Step 4)
**Verify:** `uv run pyright src/` passa sem erros de tipo nos novos métodos.

---

### Step 3 — Use cases: ToggleLike e AddLabelFeedback

**`fala-gavea/src/fala_gavea/application/use_cases/toggle_like.py`**:

```python
from __future__ import annotations
from dataclasses import dataclass
from ...domain.entities.citizen_post import CitizenPost
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


@dataclass
class ToggleLikeInput:
    post_id: str
    user_id: str


class ToggleLike:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: ToggleLikeInput) -> CitizenPost:
        if self._repo.has_liked(inp.post_id, inp.user_id):
            return self._repo.remove_like(inp.post_id, inp.user_id)
        return self._repo.add_like(inp.post_id, inp.user_id)
```

**`fala-gavea/src/fala_gavea/application/use_cases/add_label_feedback.py`**:

```python
from __future__ import annotations
from dataclasses import dataclass
from ...domain.entities.citizen_post import CitizenPost
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


@dataclass
class AddLabelFeedbackInput:
    post_id: str
    label: str
    approved: bool


class AddLabelFeedback:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: AddLabelFeedbackInput) -> CitizenPost:
        return self._repo.set_label_feedback(inp.post_id, inp.label, inp.approved)
```

- [ ] Done

**Tests:** Step 4
**Verify:** Módulos importam sem erros.

---

### Step 4 — Testes unitários e de integração

**`fala-gavea/tests/unit/application/test_citizen_post_use_cases.py`** — adicionar testes para `ToggleLike` e `AddLabelFeedback` usando mock do repositório.

Casos de teste para `ToggleLike`:
- `test_toggle_like_adds_like_when_not_liked` — `has_liked` retorna `False`, deve chamar `add_like`
- `test_toggle_like_removes_like_when_already_liked` — `has_liked` retorna `True`, deve chamar `remove_like`

Casos de teste para `AddLabelFeedback`:
- `test_add_label_feedback_calls_set_label_feedback` — verifica que chama `set_label_feedback` com os params corretos

**`fala-gavea/tests/integration/api/test_citizen_posts_api.py`** — adicionar testes de integração:
- `test_toggle_like_adds_like` — `POST /citizen_posts/{id}/likes` com `user_id` retorna 200 e `liked: true`
- `test_toggle_like_removes_like` — segundo `POST` com mesmo `user_id` retorna 200 e `liked: false`
- `test_add_label_feedback` — `POST /citizen_posts/{id}/label_feedback` retorna 200

- [ ] Done

**Tests:** `uv run pytest tests/` — todos passam
**Verify:** `uv run pytest tests/unit/application/test_citizen_post_use_cases.py tests/integration/api/test_citizen_posts_api.py -v` sem falhas.

---

### Step 5 — Schemas e endpoints

**`fala-gavea/src/fala_gavea/presentation/schemas/citizen_post_schemas.py`** — adicionar:

```python
class LikeRequest(BaseModel):
    user_id: str

class LikeResponse(BaseModel):
    post_id: str
    liked: bool
    likes_count: int

class LabelFeedbackRequest(BaseModel):
    label: str
    approved: bool
    user_id: str
```

**`fala-gavea/src/fala_gavea/presentation/api/routers/citizen_posts.py`** — adicionar 3 endpoints:

```python
@router.post("/{id}/likes", response_model=LikeResponse)
def toggle_like(id: str, body: LikeRequest, repo=Depends(get_citizen_post_repo)) -> LikeResponse:
    try:
        entity = ToggleLike(repo).execute(ToggleLikeInput(post_id=id, user_id=body.user_id))
        liked = repo.has_liked(id, body.user_id)
        return LikeResponse(post_id=id, liked=liked, likes_count=entity.likes_count)
    except (CitizenPostNotFoundError, ValueError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/label_feedback", response_model=CitizenPostResponse)
def add_label_feedback(id: str, body: LabelFeedbackRequest, repo=Depends(get_citizen_post_repo)) -> CitizenPostResponse:
    try:
        entity = AddLabelFeedback(repo).execute(AddLabelFeedbackInput(post_id=id, label=body.label, approved=body.approved))
        return CitizenPostResponse(**entity.__dict__)
    except (CitizenPostNotFoundError, ValueError) as e:
        raise HTTPException(status_code=404, detail=str(e))
```

- [ ] Done

**Tests:** Step 4 já cobre integração
**Verify:** `uvicorn fala_gavea.presentation.api.main:app --reload` sobe sem erros; `GET /docs` mostra os novos endpoints.

---

## Acceptance Criteria

- [ ] `LikeModel` criado com PK composta `(user_id, post_id)`
- [ ] `POST /citizen_posts/{id}/likes` faz toggle (segundo POST do mesmo user remove o like)
- [ ] `POST /citizen_posts/{id}/label_feedback` atualiza o campo `label_feedback` do post
- [ ] `likes_count` reflete o número real de likes na tabela `likes`
- [ ] Todos os testes passam (`uv run pytest`)
