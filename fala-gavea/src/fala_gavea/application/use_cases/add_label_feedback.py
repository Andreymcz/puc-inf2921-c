from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.citizen_post import CitizenPost
from ...domain.repositories.citizen_post_repository import CitizenPostRepository


@dataclass
class AddLabelFeedbackInput:
    post_id: str
    label: str
    approved: bool


class AddLabelFeedback:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: AddLabelFeedbackInput) -> CitizenPost:
        return self._repo.set_label_feedback(inp.post_id, inp.label, inp.approved)
