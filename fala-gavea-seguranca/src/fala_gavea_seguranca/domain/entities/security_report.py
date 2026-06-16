from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class ReportCategory(str, Enum):
    FURTO_ROUBO             = "furto_roubo"
    ILUMINACAO              = "iluminacao"
    TRANSITO                = "transito"
    ESPACO_PUBLICO_INSEGURO = "espaco_publico_inseguro"
    VANDALISMO              = "vandalismo"
    MORADORES_SITUACAO_RUA  = "moradores_situacao_rua"
    CONFLITO_SOCIAL         = "conflito_social"
    BARULHO_PERTURBACAO     = "barulho_perturbacao"
    OUTRO                   = "outro"


class ReportStatus(str, Enum):
    PENDENTE = "pendente"
    EM_ANALISE = "em_analise"
    RESOLVIDO = "resolvido"


@dataclass
class SecurityReport:
    id: str
    text: str
    category: ReportCategory
    status: ReportStatus
    author_id: str
    created_at: datetime
    lat: float | None = None
    lon: float | None = None
    territory_name: str | None = None
    photo_url: str | None = None
    ai_labels: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    ai_suggested_category: ReportCategory | None = None

    @staticmethod
    def create(
        text: str,
        category: ReportCategory,
        author_id: str,
        lat: float | None = None,
        lon: float | None = None,
        territory_name: str | None = None,
        photo_url: str | None = None,
        tags: list[str] | None = None,
    ) -> SecurityReport:
        return SecurityReport(
            id=str(uuid.uuid4()),
            text=text,
            category=category,
            status=ReportStatus.PENDENTE,
            author_id=author_id,
            created_at=datetime.now(UTC),
            lat=lat,
            lon=lon,
            territory_name=territory_name,
            photo_url=photo_url,
            tags=tags or [],
        )
