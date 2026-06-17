from __future__ import annotations

from ...domain.exceptions import CitizenPostNotFoundError
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


class DeleteCitizenPost:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> None:
        deleted = self._repo.delete(id)
        if not deleted:
            raise CitizenPostNotFoundError(id)
