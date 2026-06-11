from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.citizen_post import LikeRecord
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


@dataclass
class GetPostLikesInput:
    post_id: str


class GetPostLikes:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: GetPostLikesInput) -> list[LikeRecord]:
        return self._repo.get_likes(inp.post_id)
