from __future__ import annotations

from ...domain.entities.security_report import ReportStatus, SecurityReport
from ...domain.exceptions import InvalidInputError, SecurityReportNotFoundError
from ...domain.repositories.security_report_repository import SecurityReportRepository


class UpdateSecurityReportStatus:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, id: str, status: str) -> SecurityReport:
        try:
            new_status = ReportStatus(status)
        except ValueError:
            valid = [s.value for s in ReportStatus]
            raise InvalidInputError(f"invalid status: {status!r}. Valid: {valid}")
        entity = self._repo.update_status(id, new_status)
        if entity is None:
            raise SecurityReportNotFoundError(id)
        return entity
