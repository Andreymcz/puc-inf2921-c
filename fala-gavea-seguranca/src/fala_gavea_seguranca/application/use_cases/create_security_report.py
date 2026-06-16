from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities.security_report import ReportCategory, SecurityReport
from ...domain.exceptions import InvalidInputError
from ...domain.repositories.security_report_repository import SecurityReportRepository


@dataclass
class CreateSecurityReportInput:
    text: str
    category: str
    author_id: str
    lat: float | None = None
    lon: float | None = None
    territory_name: str | None = None
    photo_url: str | None = None


class CreateSecurityReport:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, input: CreateSecurityReportInput) -> SecurityReport:
        if not input.text or len(input.text.strip()) < 5:
            raise InvalidInputError("text must be at least 5 characters")
        try:
            category = ReportCategory(input.category)
        except ValueError:
            valid = [c.value for c in ReportCategory]
            raise InvalidInputError(f"invalid category: {input.category!r}. Valid: {valid}")
        entity = SecurityReport.create(
            text=input.text.strip(),
            category=category,
            author_id=input.author_id,
            lat=input.lat,
            lon=input.lon,
            territory_name=input.territory_name,
            photo_url=input.photo_url,
        )
        return self._repo.save(entity)
