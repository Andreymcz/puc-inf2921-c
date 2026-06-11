from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.citizen_post import CitizenPost, TerritoryLevel
from ...domain.exceptions import InvalidInputError
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


@dataclass
class CreateCitizenPostInput:
    text: str
    territory_level: str
    territory_name: str
    author_id: str


class CreateCitizenPost:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, input: CreateCitizenPostInput) -> CitizenPost:
        if not input.text or len(input.text.strip()) < 5:
            raise InvalidInputError("text must be at least 5 characters")
        try:
            level = TerritoryLevel(input.territory_level)
        except ValueError:
            raise InvalidInputError(
                f"invalid territory_level: {input.territory_level!r}"
            )
        entity = CitizenPost.create(
            text=input.text.strip(),
            territory_level=level,
            territory_name=input.territory_name,
            author_id=input.author_id,
        )
        return self._repo.save(entity)
