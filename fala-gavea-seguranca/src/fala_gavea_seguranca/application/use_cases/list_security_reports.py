from __future__ import annotations

from ...domain.entities.security_report import SecurityReport
from ...domain.repositories.security_report_repository import ReportFilter, SecurityReportRepository


class ListSecurityReports:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(
        self,
        limit: int = 50,
        offset: int = 0,
        filters: ReportFilter | None = None,
    ) -> list[SecurityReport]:
        return self._repo.find_all(limit=limit, offset=offset, filters=filters)
