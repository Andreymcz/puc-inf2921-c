import pytest

from fala_gavea_seguranca.application.use_cases.create_security_report import (
    CreateSecurityReport,
    CreateSecurityReportInput,
)
from fala_gavea_seguranca.application.use_cases.delete_security_report import DeleteSecurityReport
from fala_gavea_seguranca.application.use_cases.get_security_report import GetSecurityReport
from fala_gavea_seguranca.application.use_cases.list_security_reports import ListSecurityReports
from fala_gavea_seguranca.application.use_cases.update_security_report import UpdateSecurityReportStatus
from fala_gavea_seguranca.domain.entities.security_report import ReportCategory, ReportStatus, SecurityReport
from fala_gavea_seguranca.domain.exceptions import InvalidInputError, SecurityReportNotFoundError
from fala_gavea_seguranca.domain.repositories.security_report_repository import ReportFilter, SecurityReportRepository


class FakeRepository(SecurityReportRepository):
    def __init__(self) -> None:
        self._store: dict[str, SecurityReport] = {}

    def save(self, entity: SecurityReport) -> SecurityReport:
        self._store[entity.id] = entity
        return entity

    def find_by_id(self, id: str) -> SecurityReport | None:
        return self._store.get(id)

    def find_all(self, limit: int = 50, offset: int = 0, filters: ReportFilter | None = None) -> list[SecurityReport]:
        items = list(self._store.values())
        if filters and filters.category:
            items = [i for i in items if i.category == filters.category]
        if filters and filters.status:
            items = [i for i in items if i.status == filters.status]
        return items[offset: offset + limit]

    def update_status(self, id: str, status: ReportStatus) -> SecurityReport | None:
        if id not in self._store:
            return None
        self._store[id].status = status
        return self._store[id]

    def delete(self, id: str) -> bool:
        if id in self._store:
            del self._store[id]
            return True
        return False


VALID_INPUT = CreateSecurityReportInput(
    text="Poste apagado na rua principal da Gávea",
    category="iluminacao",
    author_id="user-123",
    lat=-22.9756,
    lon=-43.2296,
    territory_name="Gávea",
)


def test_create_happy_path() -> None:
    repo = FakeRepository()
    entity = CreateSecurityReport(repo).execute(VALID_INPUT)
    assert entity.id is not None
    assert entity.category == ReportCategory.ILUMINACAO
    assert entity.status == ReportStatus.PENDENTE
    assert entity.lat == -22.9756
    assert entity.lon == -43.2296


def test_create_short_text_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(InvalidInputError, match="5 characters"):
        CreateSecurityReport(repo).execute(
            CreateSecurityReportInput(text="Hi", category="outro", author_id="u1")
        )


def test_create_invalid_category_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(InvalidInputError, match="invalid category"):
        CreateSecurityReport(repo).execute(
            CreateSecurityReportInput(text="Valid text here", category="inexistente", author_id="u1")
        )


def test_get_found() -> None:
    repo = FakeRepository()
    created = CreateSecurityReport(repo).execute(VALID_INPUT)
    found = GetSecurityReport(repo).execute(created.id)
    assert found.id == created.id


def test_get_not_found_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(SecurityReportNotFoundError):
        GetSecurityReport(repo).execute("ghost")


def test_list_empty() -> None:
    assert ListSecurityReports(FakeRepository()).execute() == []


def test_list_multiple() -> None:
    repo = FakeRepository()
    CreateSecurityReport(repo).execute(VALID_INPUT)
    CreateSecurityReport(repo).execute(VALID_INPUT)
    assert len(ListSecurityReports(repo).execute()) == 2


def test_list_filter_category() -> None:
    repo = FakeRepository()
    CreateSecurityReport(repo).execute(VALID_INPUT)
    CreateSecurityReport(repo).execute(
        CreateSecurityReportInput(text="Buraco na pista da Lagoa", category="transito", author_id="u2")
    )
    result = ListSecurityReports(repo).execute(filters=ReportFilter(category=ReportCategory.ILUMINACAO))
    assert all(r.category == ReportCategory.ILUMINACAO for r in result)


def test_update_status() -> None:
    repo = FakeRepository()
    created = CreateSecurityReport(repo).execute(VALID_INPUT)
    updated = UpdateSecurityReportStatus(repo).execute(created.id, "em_analise")
    assert updated.status == ReportStatus.EM_ANALISE


def test_update_status_invalid_raises() -> None:
    repo = FakeRepository()
    created = CreateSecurityReport(repo).execute(VALID_INPUT)
    with pytest.raises(InvalidInputError, match="invalid status"):
        UpdateSecurityReportStatus(repo).execute(created.id, "inexistente")


def test_delete_found() -> None:
    repo = FakeRepository()
    created = CreateSecurityReport(repo).execute(VALID_INPUT)
    DeleteSecurityReport(repo).execute(created.id)
    assert repo.find_by_id(created.id) is None


def test_delete_not_found_raises() -> None:
    repo = FakeRepository()
    with pytest.raises(SecurityReportNotFoundError):
        DeleteSecurityReport(repo).execute("ghost")
