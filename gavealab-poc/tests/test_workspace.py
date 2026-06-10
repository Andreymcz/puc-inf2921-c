from __future__ import annotations
import io
import pytest
from gavealab_poc.workspace import GaveaLabWorkspace


@pytest.fixture
def ws(tmp_path):
    db = tmp_path / "test.db"
    workspace = GaveaLabWorkspace(db)
    yield workspace
    workspace.close()


CSV_SIMPLE = "text\nOlá mundo hoje\nOutro comentário aqui\nMais um relato longo o suficiente\n"


def _make_file(content: str) -> io.BytesIO:
    return io.BytesIO(content.encode())


def test_get_sessions_summary_empty(ws):
    assert ws.get_sessions_summary() == []


def test_get_sessions_summary_no_results(ws):
    ws.create_session("Sessao A", _make_file(CSV_SIMPLE))
    summary = ws.get_sessions_summary()
    assert len(summary) == 1
    s = summary[0]
    assert s["name"] == "Sessao A"
    assert s["available_results"] == []
    assert s["comment_count"] >= 1


def test_get_sessions_summary_partial_results(ws):
    session = ws.create_session("Sessao B", _make_file(CSV_SIMPLE))
    ws.save_result(session.session_id, "topic_tree", [{"topic": "Saude"}])
    summary = ws.get_sessions_summary()
    assert len(summary) == 1
    assert summary[0]["available_results"] == ["topic_tree"]


def test_get_sessions_summary_all_results(ws):
    session = ws.create_session("Sessao C", _make_file(CSV_SIMPLE))
    for rt in ["topic_tree", "claims_tree", "cruxes", "manual_categories"]:
        ws.save_result(session.session_id, rt, {})
    summary = ws.get_sessions_summary()
    assert set(summary[0]["available_results"]) == {
        "topic_tree", "claims_tree", "cruxes", "manual_categories"
    }
