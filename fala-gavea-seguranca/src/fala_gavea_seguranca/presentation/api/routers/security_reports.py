from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from fala_gavea_seguranca.application.use_cases.create_security_report import CreateSecurityReport, CreateSecurityReportInput
from fala_gavea_seguranca.application.use_cases.delete_security_report import DeleteSecurityReport
from fala_gavea_seguranca.application.use_cases.get_security_report import GetSecurityReport
from fala_gavea_seguranca.application.use_cases.list_security_reports import ListSecurityReports
from fala_gavea_seguranca.application.use_cases.update_security_report import UpdateSecurityReportStatus
from fala_gavea_seguranca.domain.exceptions import InvalidInputError, SecurityReportNotFoundError
from fala_gavea_seguranca.domain.repositories.security_report_repository import ReportFilter
from fala_gavea_seguranca.infrastructure.repositories.sqlalchemy_security_report_repository import SQLAlchemySecurityReportRepository
from fala_gavea_seguranca.application.use_cases.search_reports import SearchReports
from fala_gavea_seguranca.infrastructure.vector_store.chroma_client import delete_document, upsert_document
from fala_gavea_seguranca.presentation.api.dependencies import get_security_report_repo
from fala_gavea_seguranca.application.use_cases.auto_categorize_report import AutoCategorizeReport
from fala_gavea_seguranca.application.use_cases.set_report_category import SetReportCategory, SetReportCategoryInput
from fala_gavea_seguranca.presentation.schemas.security_report_schemas import (
    AutoCategorizeResponse,
    GeoJsonCollection,
    GeoJsonFeature,
    SearchResultResponse,
    SecurityReportCategoryUpdate,
    SecurityReportCreate,
    SecurityReportResponse,
    SecurityReportStatusUpdate,
)

router = APIRouter()


@router.post("/", response_model=SecurityReportResponse, status_code=status.HTTP_201_CREATED)
def create_security_report(
    body: SecurityReportCreate,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> SecurityReportResponse:
    try:
        entity = CreateSecurityReport(repo).execute(
            CreateSecurityReportInput(
                text=body.text,
                category=body.category,
                author_id=body.author_id,
                lat=body.lat,
                lon=body.lon,
                territory_name=body.territory_name,
                photo_url=body.photo_url,
            )
        )
        # Index in ChromaDB (best-effort — don't fail the request if unavailable)
        try:
            upsert_document(
                doc_id=entity.id,
                text=entity.text,
                metadata={
                    "type": "relato",
                    "category": entity.category.value,
                    "status": entity.status.value,
                    "lat": entity.lat,
                    "lon": entity.lon,
                    "territory_name": entity.territory_name or "",
                },
            )
        except Exception:
            pass
        return SecurityReportResponse(**entity.__dict__)
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/search", response_model=list[SearchResultResponse])
def search_reports(
    q: str = Query(..., description="Texto da busca semântica"),
    n: int = Query(10, le=50),
    category: str | None = Query(None),
    lat_min: float | None = Query(None),
    lat_max: float | None = Query(None),
    lon_min: float | None = Query(None),
    lon_max: float | None = Query(None),
) -> list[SearchResultResponse]:
    results = SearchReports().execute(
        query=q, n_results=n, category=category,
        lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max,
    )
    return [SearchResultResponse(**r.__dict__) for r in results]


@router.get("/geojson", response_model=GeoJsonCollection)
def get_geojson(
    category: str | None = Query(None),
    report_status: str | None = Query(None, alias="status"),
    since: datetime | None = Query(None),
    until: datetime | None = Query(None),
    lat_min: float | None = Query(None),
    lat_max: float | None = Query(None),
    lon_min: float | None = Query(None),
    lon_max: float | None = Query(None),
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> GeoJsonCollection:
    from fala_gavea_seguranca.domain.entities.security_report import ReportCategory, ReportStatus
    filters = ReportFilter(
        category=ReportCategory(category) if category else None,
        status=ReportStatus(report_status) if report_status else None,
        since=since,
        until=until,
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
    )
    entities = ListSecurityReports(repo).execute(limit=1000, filters=filters)
    features = [
        GeoJsonFeature(
            geometry={"type": "Point", "coordinates": [e.lon, e.lat]} if e.lat and e.lon else {"type": "Point", "coordinates": [None, None]},
            properties={
                "id": e.id,
                "text": e.text,
                "category": e.category.value,
                "status": e.status.value,
                "territory_name": e.territory_name,
                "author_id": e.author_id,
                "created_at": e.created_at.isoformat(),
                "ai_suggested_category": e.ai_suggested_category.value if e.ai_suggested_category else None,
            },
        )
        for e in entities
    ]
    return GeoJsonCollection(features=features)


@router.get("/", response_model=list[SecurityReportResponse])
def list_security_reports(
    limit: int = 50,
    offset: int = 0,
    category: str | None = Query(None),
    report_status: str | None = Query(None, alias="status"),
    since: datetime | None = Query(None),
    until: datetime | None = Query(None),
    lat_min: float | None = Query(None),
    lat_max: float | None = Query(None),
    lon_min: float | None = Query(None),
    lon_max: float | None = Query(None),
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> list[SecurityReportResponse]:
    from fala_gavea_seguranca.domain.entities.security_report import ReportCategory, ReportStatus
    filters = ReportFilter(
        category=ReportCategory(category) if category else None,
        status=ReportStatus(report_status) if report_status else None,
        since=since,
        until=until,
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
    )
    entities = ListSecurityReports(repo).execute(limit=limit, offset=offset, filters=filters)
    return [SecurityReportResponse(**e.__dict__) for e in entities]


@router.get("/{id}", response_model=SecurityReportResponse)
def get_security_report(
    id: str,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> SecurityReportResponse:
    try:
        entity = GetSecurityReport(repo).execute(id)
        return SecurityReportResponse(**entity.__dict__)
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id}/status", response_model=SecurityReportResponse)
def update_security_report_status(
    id: str,
    body: SecurityReportStatusUpdate,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> SecurityReportResponse:
    try:
        entity = UpdateSecurityReportStatus(repo).execute(id, body.status)
        return SecurityReportResponse(**entity.__dict__)
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_security_report(
    id: str,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> None:
    try:
        DeleteSecurityReport(repo).execute(id)
        try:
            delete_document(id)
        except Exception:
            pass
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{id}/auto_categorize", response_model=AutoCategorizeResponse)
def auto_categorize(
    id: str,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> AutoCategorizeResponse:
    try:
        result = AutoCategorizeReport(repo).execute(id)
        return AutoCategorizeResponse(
            category=result.category,
            confidence=result.confidence,
            justification=result.justification,
        )
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.patch("/{id}/category", response_model=SecurityReportResponse)
def set_category(
    id: str,
    body: SecurityReportCategoryUpdate,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> SecurityReportResponse:
    try:
        entity = SetReportCategory(repo).execute(SetReportCategoryInput(id=id, category=body.category))
        return SecurityReportResponse(**entity.__dict__)
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
