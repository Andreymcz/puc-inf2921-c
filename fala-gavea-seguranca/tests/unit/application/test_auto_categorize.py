from __future__ import annotations

import json
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from fala_gavea_seguranca.application.use_cases.auto_categorize_report import AutoCategorizeReport
from fala_gavea_seguranca.application.use_cases.set_report_category import SetReportCategory, SetReportCategoryInput
from fala_gavea_seguranca.domain.entities.security_report import ReportCategory, ReportStatus, SecurityReport
from fala_gavea_seguranca.domain.exceptions import InvalidInputError, SecurityReportNotFoundError


def _make_report(category: ReportCategory = ReportCategory.ILUMINACAO) -> SecurityReport:
    return SecurityReport(
        id="report-1",
        text="Poste apagado na esquina",
        category=category,
        status=ReportStatus.PENDENTE,
        author_id="user-1",
        created_at=datetime.now(UTC),
    )


def _make_repo(report: SecurityReport | None = None) -> MagicMock:
    repo = MagicMock()
    repo.find_by_id.return_value = report
    repo.update_ai_suggested_category.return_value = report
    repo.update_category.return_value = report
    return repo


# --- AutoCategorizeReport ---

def test_auto_categorize_success() -> None:
    report = _make_report()
    repo = _make_repo(report)
    valid_response = json.dumps({"category": "furto_roubo", "confidence": "alta", "justification": "Relato de roubo"})

    with patch("fala_gavea_seguranca.application.use_cases.auto_categorize_report.chat_completion", return_value=valid_response):
        result = AutoCategorizeReport(repo).execute("report-1")

    assert result.category == "furto_roubo"
    assert result.confidence == "alta"
    assert result.justification == "Relato de roubo"
    repo.update_ai_suggested_category.assert_called_once_with("report-1", ReportCategory.FURTO_ROUBO)


def test_auto_categorize_invalid_json() -> None:
    report = _make_report()
    repo = _make_repo(report)

    with patch("fala_gavea_seguranca.application.use_cases.auto_categorize_report.chat_completion", return_value="não é json"):
        with pytest.raises(ValueError, match="Resposta inválida"):
            AutoCategorizeReport(repo).execute("report-1")


def test_auto_categorize_invalid_category() -> None:
    report = _make_report()
    repo = _make_repo(report)
    bad_response = json.dumps({"category": "categoria_inexistente", "confidence": "alta", "justification": "x"})

    with patch("fala_gavea_seguranca.application.use_cases.auto_categorize_report.chat_completion", return_value=bad_response):
        with pytest.raises(ValueError, match="Resposta inválida"):
            AutoCategorizeReport(repo).execute("report-1")


def test_auto_categorize_not_found() -> None:
    repo = _make_repo(None)

    with patch("fala_gavea_seguranca.application.use_cases.auto_categorize_report.chat_completion"):
        with pytest.raises(SecurityReportNotFoundError):
            AutoCategorizeReport(repo).execute("nonexistent")


# --- SetReportCategory ---

def test_set_report_category_success() -> None:
    report = _make_report()
    updated = SecurityReport(
        id=report.id, text=report.text,
        category=ReportCategory.FURTO_ROUBO,
        status=report.status, author_id=report.author_id, created_at=report.created_at,
        ai_suggested_category=None,
    )
    repo = MagicMock()
    repo.update_category.return_value = updated

    result = SetReportCategory(repo).execute(SetReportCategoryInput(id="report-1", category="furto_roubo"))

    assert result.category == ReportCategory.FURTO_ROUBO
    assert result.ai_suggested_category is None
    repo.update_category.assert_called_once_with("report-1", ReportCategory.FURTO_ROUBO)


def test_set_report_category_invalid() -> None:
    repo = MagicMock()

    with pytest.raises(InvalidInputError, match="Categoria inválida"):
        SetReportCategory(repo).execute(SetReportCategoryInput(id="report-1", category="categoria_errada"))


def test_set_report_category_not_found() -> None:
    repo = MagicMock()
    repo.update_category.return_value = None

    with pytest.raises(SecurityReportNotFoundError):
        SetReportCategory(repo).execute(SetReportCategoryInput(id="nonexistent", category="furto_roubo"))
