from __future__ import annotations

from ...domain.exceptions import SecurityReportNotFoundError
from ...domain.repositories.security_report_repository import SecurityReportRepository


class DeleteSecurityReport:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> None:
        deleted = self._repo.delete(id)
        if not deleted:
            raise SecurityReportNotFoundError(id)
