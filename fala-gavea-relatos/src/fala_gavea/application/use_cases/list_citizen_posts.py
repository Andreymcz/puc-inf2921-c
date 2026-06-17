from __future__ import annotations

from ...domain.entities.citizen_post import CitizenPost
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


class ListCitizenPosts:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, limit: int = 50, offset: int = 0) -> list[CitizenPost]:
        return self._repo.find_all(limit=limit, offset=offset)
