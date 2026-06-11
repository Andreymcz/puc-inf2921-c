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
