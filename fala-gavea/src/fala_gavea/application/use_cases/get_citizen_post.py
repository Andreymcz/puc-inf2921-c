from __future__ import annotations

from ...domain.entities.citizen_post import CitizenPost
from ...domain.exceptions import CitizenPostNotFoundError
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


class GetCitizenPost:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> CitizenPost:
        entity = self._repo.find_by_id(id)
        if entity is None:
            raise CitizenPostNotFoundError(id)
        return entity
