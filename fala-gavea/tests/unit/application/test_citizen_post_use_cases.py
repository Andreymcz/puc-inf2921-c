import pytest

from fala_gavea.application.use_cases.create_citizen_post import (
    CreateCitizenPost,
    CreateCitizenPostInput,
)
from fala_gavea.application.use_cases.delete_citizen_post import DeleteCitizenPost
from fala_gavea.application.use_cases.get_citizen_post import GetCitizenPost
from fala_gavea.application.use_cases.list_citizen_posts import ListCitizenPosts
from fala_gavea.domain.entities.citizen_post import CitizenPost
from fala_gavea.domain.exceptions import (
    CitizenPostNotFoundError,
    InvalidInputError,
)
from fala_gavea.domain.repositories.citizen_post_repository import CitizenPostRepository


class FakeRepository(CitizenPostRepository):
    """In-memory fake repository for unit testing."""

    def __init__(self) -> None:
        self._store: dict[str, CitizenPost] = {}

    def save(self, entity: CitizenPost) -> CitizenPost:
        self._store[entity.id] = entity
        return entity

    def find_by_id(self, id: str) -> CitizenPost | None:
        return self._store.get(id)

    def find_all(self, limit: int = 50, offset: int = 0) -> list[CitizenPost]:
        items = list(self._store.values())
        return items[offset : offset + limit]

    def delete(self, id: str) -> bool:
        if id in self._store:
            del self._store[id]
            return True
        return False


VALID_INPUT = CreateCitizenPostInput(
    text="Precisa de mais iluminação na rua principal",
    territory_level="neighborhood",
    territory_name="Gávea",
    author_id="user-123",
)


# ── CreateCitizenPost ──────────────────────────────────────────────────────


def test_create_citizen_post_happy_path() -> None:
    repo = FakeRepository()
    entity = CreateCitizenPost(repo).execute(VALID_INPUT)
    assert entity.id is not None
    assert entity.text == VALID_INPUT.text.strip()
    assert entity.territory_level.value == "neighborhood"


def test_create_citizen_post_short_text_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(InvalidInputError, match="5 characters"):
        CreateCitizenPost(repo).execute(
            CreateCitizenPostInput(
                text="Hi",
                territory_level="city",
                territory_name="Rio",
                author_id="u1",
            )
        )


def test_create_citizen_post_invalid_territory_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(InvalidInputError, match="invalid territory_level"):
        CreateCitizenPost(repo).execute(
            CreateCitizenPostInput(
                text="Valid text here",
                territory_level="galaxy",
                territory_name="Milky Way",
                author_id="u1",
            )
        )


# ── GetCitizenPost ─────────────────────────────────────────────────────────


def test_get_citizen_post_found() -> None:
    repo = FakeRepository()
    created = CreateCitizenPost(repo).execute(VALID_INPUT)
    found = GetCitizenPost(repo).execute(created.id)
    assert found.id == created.id


def test_get_citizen_post_not_found_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(CitizenPostNotFoundError):
        GetCitizenPost(repo).execute("does-not-exist")


# ── ListCitizenPosts ───────────────────────────────────────────────────────


def test_list_citizen_posts_empty() -> None:
    repo = FakeRepository()
    assert ListCitizenPosts(repo).execute() == []


def test_list_citizen_posts_multiple() -> None:
    repo = FakeRepository()
    CreateCitizenPost(repo).execute(VALID_INPUT)
    CreateCitizenPost(repo).execute(VALID_INPUT)
    assert len(ListCitizenPosts(repo).execute()) == 2


def test_list_citizen_posts_pagination() -> None:
    repo = FakeRepository()
    for _ in range(5):
        CreateCitizenPost(repo).execute(VALID_INPUT)
    page = ListCitizenPosts(repo).execute(limit=2, offset=1)
    assert len(page) == 2


# ── DeleteCitizenPost ─────────────────────────────────────────────────────


def test_delete_citizen_post_found() -> None:
    repo = FakeRepository()
    created = CreateCitizenPost(repo).execute(VALID_INPUT)
    DeleteCitizenPost(repo).execute(created.id)
    assert repo.find_by_id(created.id) is None


def test_delete_citizen_post_not_found_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(CitizenPostNotFoundError):
        DeleteCitizenPost(repo).execute("ghost-id")
