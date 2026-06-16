from __future__ import annotations

from sqlalchemy.orm import Session

from ...domain.entities.security_report import ReportCategory, ReportStatus, SecurityReport
from ...domain.repositories.security_report_repository import ReportFilter, SecurityReportRepository
from ..database.models import SecurityReportModel


class SQLAlchemySecurityReportRepository(SecurityReportRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, entity: SecurityReport) -> SecurityReport:
        self._session.merge(self._to_model(entity))
        self._session.commit()
        return entity

    def find_by_id(self, id: str) -> SecurityReport | None:
        model = self._session.get(SecurityReportModel, id)
        return self._to_entity(model) if model else None

    def find_all(
        self,
        limit: int = 50,
        offset: int = 0,
        filters: ReportFilter | None = None,
    ) -> list[SecurityReport]:
        q = self._session.query(SecurityReportModel)
        if filters:
            if filters.category:
                q = q.filter(SecurityReportModel.category == filters.category)
            if filters.status:
                q = q.filter(SecurityReportModel.status == filters.status)
            if filters.since:
                q = q.filter(SecurityReportModel.created_at >= filters.since)
            if filters.until:
                q = q.filter(SecurityReportModel.created_at <= filters.until)
            if filters.lat_min is not None:
                q = q.filter(SecurityReportModel.lat >= filters.lat_min)
            if filters.lat_max is not None:
                q = q.filter(SecurityReportModel.lat <= filters.lat_max)
            if filters.lon_min is not None:
                q = q.filter(SecurityReportModel.lon >= filters.lon_min)
            if filters.lon_max is not None:
                q = q.filter(SecurityReportModel.lon <= filters.lon_max)
            if filters.tag is not None:
                # Use LIKE with quoted value to match exact JSON string elements
                # (avoids false positives from substring matching on serialized JSON)
                q = q.filter(SecurityReportModel.tags.like(f'%"{filters.tag}"%'))
        models = (
            q.order_by(SecurityReportModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]

    def update_tags(self, id: str, tags: list[str]) -> SecurityReport | None:
        model = self._session.get(SecurityReportModel, id)
        if model is None:
            return None
        model.tags = tags
        self._session.commit()
        return self._to_entity(model)

    def update_status(self, id: str, status: ReportStatus) -> SecurityReport | None:
        model = self._session.get(SecurityReportModel, id)
        if model is None:
            return None
        model.status = status
        self._session.commit()
        return self._to_entity(model)

    def delete(self, id: str) -> bool:
        model = self._session.get(SecurityReportModel, id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.commit()
        return True

    def update_ai_suggested_category(self, id: str, category: ReportCategory | None) -> SecurityReport | None:
        model = self._session.get(SecurityReportModel, id)
        if model is None:
            return None
        model.ai_suggested_category = category
        self._session.commit()
        return self._to_entity(model)

    def update_category(self, id: str, category: ReportCategory) -> SecurityReport | None:
        model = self._session.get(SecurityReportModel, id)
        if model is None:
            return None
        model.category = category
        model.ai_suggested_category = None
        self._session.commit()
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: SecurityReportModel) -> SecurityReport:
        return SecurityReport(
            id=model.id,
            text=model.text,
            category=ReportCategory(model.category),
            status=ReportStatus(model.status),
            author_id=model.author_id,
            created_at=model.created_at,
            lat=model.lat,
            lon=model.lon,
            territory_name=model.territory_name,
            photo_url=model.photo_url,
            ai_labels=model.ai_labels or [],
            tags=model.tags or [],
            ai_suggested_category=ReportCategory(model.ai_suggested_category) if model.ai_suggested_category else None,
        )

    @staticmethod
    def _to_model(entity: SecurityReport) -> SecurityReportModel:
        return SecurityReportModel(
            id=entity.id,
            text=entity.text,
            category=entity.category,
            status=entity.status,
            author_id=entity.author_id,
            created_at=entity.created_at,
            lat=entity.lat,
            lon=entity.lon,
            territory_name=entity.territory_name,
            photo_url=entity.photo_url,
            ai_labels=entity.ai_labels,
            tags=entity.tags,
            ai_suggested_category=entity.ai_suggested_category,
        )
