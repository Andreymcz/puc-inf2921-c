# Plan 000060 | FEATURE-B | 2026-06-16 14:03 UTC | Tags livres em SecurityReport | Review: light
plan_format_version: 1

## Brief

> roadmap-000056 Wave 1 Item 2 — Tags livres: campo `tags: list[str]` em `SecurityReport`, endpoint `PATCH /{id}/tags`, filtro `?tag=` no geojson, exibição de tags no response.

## Agent Interpretation

Adicionar suporte a tags livres (strings arbitrárias) nos relatos de segurança. Tags são atribuídas via API (`PATCH /security_reports/{id}/tags`) e filtráveis no endpoint geojson (`?tag=valor`). O campo é incluído no `SecurityReportResponse` e nas propriedades do GeoJSON. Segue o padrão de arquitetura existente: domain entity → repository → use case → router → schema.

---

## Scope

- **In scope**: Campo `tags` na entidade, modelo DB, response schema; use case `SetReportTags`; endpoint `PATCH /{id}/tags`; filtro `?tag=` no geojson e list; exposição de `tags` nas properties do geojson; `tag` em `ReportFilter`.
- **Out of scope**: Interface frontend (Wave 2, plan-000063); lógica de tag sugerida por IA (Wave 1 Item 3, plan-000061).

---

## Files

- `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py` — adicionar `tags: list[str]`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/repositories/security_report_repository.py` — adicionar `tag: str | None` a `ReportFilter`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/database/models.py` — coluna `tags JSON`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/repositories/sqlalchemy_security_report_repository.py` — filtro por tag + `update_tags`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/application/use_cases/set_report_tags.py` — novo use case
- `fala-gavea-seguranca/src/fala_gavea_seguranca/application/use_cases/__init__.py` — sem alteração (módulo já existe)
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/schemas/security_report_schemas.py` — `SecurityReportTagsUpdate`, `tags` em `SecurityReportResponse`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/security_reports.py` — novo endpoint `PATCH /{id}/tags`, filtro `?tag=` no geojson e list, `tags` nas properties do geojson
- `fala-gavea-seguranca/tests/unit/application/test_security_report_use_cases.py` — testes para `SetReportTags`
- `fala-gavea-seguranca/tests/integration/api/test_security_reports_api.py` — teste do endpoint `PATCH /{id}/tags` e filtro `?tag=`

---

## Steps

### Step 1: Adicionar campo `tags` à entidade de domínio e ao `ReportFilter`

Atualizar `domain/entities/security_report.py`: adicionar `tags: list[str] = field(default_factory=list)` ao dataclass `SecurityReport`. O campo já existe como `ai_labels` com o mesmo tipo; o campo `tags` é independente (tags curadas por cidadão/operador, não por IA).

Atualizar `domain/repositories/security_report_repository.py`: adicionar `tag: str | None = None` ao dataclass `ReportFilter`.

Atualizar `SecurityReport.create()` para aceitar `tags: list[str] | None = None` e passá-lo para o constructor (ou manter `tags=[]` como default — preferir default vazio para não quebrar callsites existentes).

- **Files**: `domain/entities/security_report.py`, `domain/repositories/security_report_repository.py`
- **Interface**: `SecurityReport.tags: list[str]`; `ReportFilter.tag: str | None`
- **Verify**: `uv run python -c "from fala_gavea_seguranca.domain.entities.security_report import SecurityReport; r = SecurityReport.create('Teste','outro','u1'); print(r.tags)"` imprime `[]`
- **Tests**: verificado implicitamente pelos demais steps
- [ ] Done

### Step 2: Adicionar coluna `tags` ao modelo SQLAlchemy e ao mapeamento

Atualizar `infrastructure/database/models.py`: adicionar `tags = Column(JSON, nullable=False, default=list)` em `SecurityReportModel` (mesmo padrão de `ai_labels`).

Atualizar `infrastructure/repositories/sqlalchemy_security_report_repository.py`:
- `_to_entity`: incluir `tags=model.tags or []`
- `_to_model`: incluir `tags=entity.tags`
- Novo método `update_tags(self, id: str, tags: list[str]) -> SecurityReport | None`: busca o model, atualiza `model.tags = tags`, faz commit, retorna entidade.
- Filtro em `find_all`: se `filters.tag` estiver preenchido, aplicar `q = q.filter(SecurityReportModel.tags.contains(filters.tag))` — compatível com SQLite JSON column (usa `LIKE '%"tag"%'` internamente via SQLAlchemy `contains`).

Como o projeto usa `Base.metadata.create_all()` no startup (sem Alembic), basta deletar `app.db` após a mudança para que o schema seja recriado.

- **Files**: `infrastructure/database/models.py`, `infrastructure/repositories/sqlalchemy_security_report_repository.py`
- **Interface**: `SQLAlchemySecurityReportRepository.update_tags(id, tags) -> SecurityReport | None`
- **Verify**: reiniciar servidor após deletar `app.db`; POST de novo relato inclui `tags: []` no response
- **Tests**: Step 4 cobre integração
- [ ] Done

### Step 3: Criar use case `SetReportTags`

Criar `application/use_cases/set_report_tags.py`:

```python
from __future__ import annotations
from dataclasses import dataclass
from ..domain.repositories.security_report_repository import SecurityReportRepository
from ..domain.exceptions import SecurityReportNotFoundError

@dataclass
class SetReportTagsInput:
    id: str
    tags: list[str]

class SetReportTags:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, input: SetReportTagsInput):
        entity = self._repo.update_tags(input.id, input.tags)
        if entity is None:
            raise SecurityReportNotFoundError(f"Report {input.id} not found")
        return entity
```

Nota: `SecurityReportRepository` (ABC) deve declarar `update_tags` como `@abstractmethod`. Atualizar o ABC e a implementação SQLAlchemy de forma consistente.

- **Files**: `application/use_cases/set_report_tags.py` (create), `domain/repositories/security_report_repository.py` (add abstract method)
- **Interface**: `SetReportTags(repo).execute(SetReportTagsInput(id, tags)) -> SecurityReport`
- **Verify**: importar sem erro
- **Tests**: Step 4
- [ ] Done

### Step 4: Adicionar schema `SecurityReportTagsUpdate` e atualizar `SecurityReportResponse`

Em `presentation/schemas/security_report_schemas.py`:
- Adicionar `class SecurityReportTagsUpdate(BaseModel): tags: list[str]`
- Adicionar `tags: list[str]` a `SecurityReportResponse`

- **Files**: `presentation/schemas/security_report_schemas.py`
- **Interface**: `SecurityReportTagsUpdate`, `SecurityReportResponse.tags`
- [ ] Done

### Step 5: Adicionar endpoint `PATCH /{id}/tags` e filtro `?tag=` no router

Em `presentation/api/routers/security_reports.py`:

1. Importar `SetReportTags`, `SetReportTagsInput`, `SecurityReportTagsUpdate`.

2. Novo endpoint:
```python
@router.patch("/{id}/tags", response_model=SecurityReportResponse)
def set_report_tags(
    id: str,
    body: SecurityReportTagsUpdate,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> SecurityReportResponse:
    try:
        entity = SetReportTags(repo).execute(SetReportTagsInput(id=id, tags=body.tags))
        return SecurityReportResponse(**entity.__dict__)
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
```

3. Adicionar `tag: str | None = Query(None)` ao `get_geojson` e ao `list_security_reports`. Passá-lo para `ReportFilter(tag=tag, ...)`.

4. Em `get_geojson`, adicionar `"tags": e.tags` e `"ai_labels": e.ai_labels` às properties de cada feature (para uso futuro pelo frontend). O campo `tags` é lista; o frontend exibe como chips.

- **Files**: `presentation/api/routers/security_reports.py`
- **Interface**: `PATCH /security_reports/{id}/tags`, `GET /security_reports/geojson?tag=valor`
- **Verify**: `curl -X PATCH http://localhost:8000/security_reports/<id>/tags -H 'Content-Type: application/json' -d '{"tags":["perigoso","noite"]}'` retorna o relato com `tags: ["perigoso","noite"]`; `GET /geojson?tag=perigoso` retorna apenas relatos com essa tag
- **Tests**: Step 6
- [ ] Done

### Step 6: Testes

**Unit** — `tests/unit/application/test_security_report_use_cases.py`:
- `test_set_report_tags_success`: mock repo que retorna entidade atualizada; verifica que `update_tags` foi chamado com os valores corretos.
- `test_set_report_tags_not_found`: mock repo retornando `None`; verifica que `SecurityReportNotFoundError` é levantado.

**Integration** — `tests/integration/api/test_security_reports_api.py`:
- `test_patch_tags`: cria relato, aplica `PATCH /{id}/tags`, verifica response com `tags` corretos.
- `test_get_geojson_filter_tag`: cria dois relatos com tags distintas, verifica que `?tag=X` retorna apenas o correto.

- **Files**: `tests/unit/application/test_security_report_use_cases.py`, `tests/integration/api/test_security_reports_api.py`
- **Verify**: `cd fala-gavea-seguranca && uv run pytest tests/ -k "tag" -v` passa
- [ ] Done

---

## Review

### Perspectives evaluated

| Tag | Perspective | Status | Notes |
|-----|-------------|--------|-------|
| ARCH | Architecture | Adopted | Segue padrão entity → repo → use case → router → schema; sem desvio |
| DATA | Data Integrity | Adopted | JSON column com default `list`; filtro usa `contains` compatível com SQLite |
| SEC | Security | Adopted | Tags são strings livres; nenhuma execução de código; filtro via ORM (sem SQL injection) |
| TEST | Testability | Adopted | Use case mockável; integração com TestClient |

---

## Commit message

```
feat(security-report): add free-text tags — PATCH /{id}/tags + ?tag= filter

Add tags: list[str] to SecurityReport entity, DB model, and response
schema. New use case SetReportTags and PATCH /security_reports/{id}/tags
endpoint. Adds ?tag= filter to GET /geojson and GET / endpoints.
GeoJSON features now include tags and ai_labels properties.

Part of roadmap-000056 Wave 1 Item 2.
```
