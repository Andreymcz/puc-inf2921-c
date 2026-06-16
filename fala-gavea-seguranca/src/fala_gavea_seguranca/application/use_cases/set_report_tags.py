from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.security_report import SecurityReport
from ...domain.exceptions import SecurityReportNotFoundError
from ...domain.repositories.security_report_repository import SecurityReportRepository


@dataclass
class SetReportTagsInput:
    id: str
    tags: list[str]


class SetReportTags:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, input: SetReportTagsInput) -> SecurityReport:
        entity = self._repo.update_tags(input.id, input.tags)
        if entity is None:
            raise SecurityReportNotFoundError(input.id)
        return entity
