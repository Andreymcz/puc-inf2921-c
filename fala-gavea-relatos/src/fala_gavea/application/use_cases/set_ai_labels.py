from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.citizen_post import CitizenPost
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


@dataclass
class SetAiLabelsInput:
    post_id: str
    labels: list[str]


class SetAiLabels:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: SetAiLabelsInput) -> CitizenPost:
        return self._repo.set_ai_labels(inp.post_id, inp.labels)
