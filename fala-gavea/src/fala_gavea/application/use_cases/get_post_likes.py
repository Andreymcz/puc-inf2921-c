from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.citizen_post import LikeRecord
from ...domain.exceptions import CitizenPostNotFoundError
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


@dataclass
class GetPostLikesInput:
    post_id: str


class GetPostLikes:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: GetPostLikesInput) -> list[LikeRecord]:
        if self._repo.find_by_id(inp.post_id) is None:
            raise CitizenPostNotFoundError(f"CitizenPost with id '{inp.post_id}' not found")
        return self._repo.get_likes(inp.post_id)
