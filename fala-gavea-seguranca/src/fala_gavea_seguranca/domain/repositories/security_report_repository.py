from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from ..entities.security_report import ReportCategory, ReportStatus, SecurityReport


@dataclass
class ReportFilter:
    category: ReportCategory | None = None
    status: ReportStatus | None = None
    since: datetime | None = None
    until: datetime | None = None
    lat_min: float | None = None
    lat_max: float | None = None
    lon_min: float | None = None
    lon_max: float | None = None
    tag: str | None = None


class SecurityReportRepository(ABC):
    @abstractmethod
    def save(self, entity: SecurityReport) -> SecurityReport: ...

    @abstractmethod
    def find_by_id(self, id: str) -> SecurityReport | None: ...

    @abstractmethod
    def find_all(
        self,
        limit: int = 50,
        offset: int = 0,
        filters: ReportFilter | None = None,
    ) -> list[SecurityReport]: ...

    @abstractmethod
    def update_status(self, id: str, status: ReportStatus) -> SecurityReport | None: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

    @abstractmethod
    def update_ai_suggested_category(self, id: str, category: ReportCategory | None) -> SecurityReport | None: ...

    @abstractmethod
    def update_category(self, id: str, category: ReportCategory) -> SecurityReport | None: ...

    @abstractmethod
    def update_tags(self, id: str, tags: list[str]) -> SecurityReport | None: ...
