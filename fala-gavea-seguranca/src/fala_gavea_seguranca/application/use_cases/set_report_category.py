from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.security_report import ReportCategory, SecurityReport
from ...domain.exceptions import InvalidInputError, SecurityReportNotFoundError
from ...domain.repositories.security_report_repository import SecurityReportRepository


@dataclass
class SetReportCategoryInput:
    id: str
    category: str


class SetReportCategory:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, input: SetReportCategoryInput) -> SecurityReport:
        try:
            category = ReportCategory(input.category)
        except ValueError:
            raise InvalidInputError(f"Categoria inválida: {input.category!r}")

        entity = self._repo.update_category(input.id, category)
        if entity is None:
            raise SecurityReportNotFoundError(input.id)
        return entity
