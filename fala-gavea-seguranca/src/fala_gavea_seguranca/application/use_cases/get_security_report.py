from __future__ import annotations

from ...domain.entities.security_report import SecurityReport
from ...domain.exceptions import SecurityReportNotFoundError
from ...domain.repositories.security_report_repository import SecurityReportRepository


class GetSecurityReport:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> SecurityReport:
        entity = self._repo.find_by_id(id)
        if entity is None:
            raise SecurityReportNotFoundError(id)
        return entity
