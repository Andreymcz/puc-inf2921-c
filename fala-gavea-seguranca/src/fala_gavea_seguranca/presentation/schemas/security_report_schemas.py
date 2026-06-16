from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_validator


class SecurityReportCreate(BaseModel):
    text: str
    category: str
    author_id: str
    lat: float | None = None
    lon: float | None = None
    territory_name: str | None = None
    photo_url: str | None = None

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("text must not be empty")
        return v


class SecurityReportStatusUpdate(BaseModel):
    status: str


class SecurityReportCategoryUpdate(BaseModel):
    category: str


class SecurityReportTagsUpdate(BaseModel):
    tags: list[str]


class AutoCategorizeResponse(BaseModel):
    category: str
    confidence: str
    justification: str


class SecurityReportResponse(BaseModel):
    id: str
    text: str
    category: str
    status: str
    author_id: str
    created_at: datetime
    lat: float | None
    lon: float | None
    territory_name: str | None
    photo_url: str | None
    ai_labels: list[str]
    ai_suggested_category: str | None = None
    tags: list[str] = []

    model_config = {"from_attributes": True}


class SearchResultResponse(BaseModel):
    id: str
    text: str
    category: str
    status: str
    distance: float
    lat: float | None
    lon: float | None
    territory_name: str | None

    model_config = {"from_attributes": True}


class GeoJsonFeature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: dict


class GeoJsonCollection(BaseModel):
    type: str = "FeatureCollection"
    features: list[GeoJsonFeature]
