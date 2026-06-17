from __future__ import annotations

from ...domain.entities.citizen_post import CitizenPost, TerritoryLevel
from ...domain.exceptions import InvalidInputError
from ...domain.repositories.citizen_post_repository import CitizenPostRepository
from .create_citizen_post import CreateCitizenPostInput


class BulkCreateCitizenPosts:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inputs: list[CreateCitizenPostInput]) -> list[CitizenPost]:
        entities: list[CitizenPost] = []
        for inp in inputs:
            if not inp.text or len(inp.text.strip()) < 5:
                raise InvalidInputError("text must be at least 5 characters")
            try:
                level = TerritoryLevel(inp.territory_level)
            except ValueError:
                raise InvalidInputError(
                    f"invalid territory_level: {inp.territory_level!r}"
                )
            entities.append(
                CitizenPost.create(
                    text=inp.text.strip(),
                    territory_level=level,
                    territory_name=inp.territory_name,
                    author_id=inp.author_id,
                )
            )
        if not entities:
            return []
        return self._repo.save_many(entities)
