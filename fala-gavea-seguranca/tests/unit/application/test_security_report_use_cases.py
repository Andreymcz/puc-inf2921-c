import pytest
from datetime import datetime, timezone

from fala_gavea_seguranca.application.use_cases.create_security_report import (
    CreateSecurityReport,
    CreateSecurityReportInput,
)
from fala_gavea_seguranca.application.use_cases.delete_security_report import DeleteSecurityReport
from fala_gavea_seguranca.application.use_cases.get_security_report import GetSecurityReport
from fala_gavea_seguranca.application.use_cases.list_security_reports import ListSecurityReports
from fala_gavea_seguranca.application.use_cases.set_report_tags import SetReportTags, SetReportTagsInput
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
        if filters:
            if filters.category:
                items = [i for i in items if i.category == filters.category]
            if filters.status:
                items = [i for i in items if i.status == filters.status]
            if filters.since:
                items = [i for i in items if i.created_at >= filters.since]
            if filters.until:
                items = [i for i in items if i.created_at <= filters.until]
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

    def update_ai_suggested_category(self, id: str, category: ReportCategory | None) -> SecurityReport | None:
        if id not in self._store:
            return None
        self._store[id].ai_suggested_category = category
        return self._store[id]

    def update_category(self, id: str, category: ReportCategory) -> SecurityReport | None:
        if id not in self._store:
            return None
        self._store[id].category = category
        return self._store[id]

    def update_tags(self, id: str, tags: list[str]) -> SecurityReport | None:
        if id not in self._store:
            return None
        self._store[id].tags = tags
        return self._store[id]


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


def _make_report(created_at: datetime) -> SecurityReport:
    return SecurityReport(
        id=str(__import__("uuid").uuid4()),
        text="Relato de teste para filtro temporal",
        category=ReportCategory.ILUMINACAO,
        status=ReportStatus.PENDENTE,
        author_id="user-test",
        created_at=created_at,
    )


def test_filter_since_until_range() -> None:
    repo = FakeRepository()
    jan = datetime(2026, 1, 15, tzinfo=timezone.utc)
    mar = datetime(2026, 3, 15, tzinfo=timezone.utc)
    jun = datetime(2026, 6, 15, tzinfo=timezone.utc)
    for dt in (jan, mar, jun):
        repo._store[str(__import__("uuid").uuid4())] = _make_report(dt)

    result = ListSecurityReports(repo).execute(
        filters=ReportFilter(
            since=datetime(2026, 2, 1, tzinfo=timezone.utc),
            until=datetime(2026, 4, 30, tzinfo=timezone.utc),
        )
    )
    assert len(result) == 1
    assert result[0].created_at == mar


def test_filter_until_only() -> None:
    repo = FakeRepository()
    jan = datetime(2026, 1, 15, tzinfo=timezone.utc)
    jun = datetime(2026, 6, 15, tzinfo=timezone.utc)
    for dt in (jan, jun):
        repo._store[str(__import__("uuid").uuid4())] = _make_report(dt)

    result = ListSecurityReports(repo).execute(
        filters=ReportFilter(until=datetime(2026, 3, 31, tzinfo=timezone.utc))
    )
    assert len(result) == 1
    assert result[0].created_at == jan


def test_set_report_tags_success() -> None:
    repo = FakeRepository()
    created = CreateSecurityReport(repo).execute(VALID_INPUT)
    new_tags = ["urgente", "verificado"]
    updated = SetReportTags(repo).execute(SetReportTagsInput(id=created.id, tags=new_tags))
    assert updated.tags == new_tags
    assert repo.find_by_id(created.id).tags == new_tags


def test_set_report_tags_not_found() -> None:
    repo = FakeRepository()
    with pytest.raises(SecurityReportNotFoundError):
        SetReportTags(repo).execute(SetReportTagsInput(id="ghost", tags=["x"]))
