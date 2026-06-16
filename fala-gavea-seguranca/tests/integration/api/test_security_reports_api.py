from fastapi.testclient import TestClient

VALID_PAYLOAD = {
    "text": "Poste apagado na Rua Marquês de São Vicente",
    "category": "iluminacao",
    "author_id": "user-abc",
    "lat": -22.9756,
    "lon": -43.2296,
    "territory_name": "Gávea",
}


def test_create_returns_201(client: TestClient) -> None:
    response = client.post("/security_reports/", json=VALID_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == VALID_PAYLOAD["text"]
    assert data["category"] == "iluminacao"
    assert data["status"] == "pendente"
    assert data["lat"] == -22.9756
    assert "id" in data


def test_create_empty_text_returns_422(client: TestClient) -> None:
    response = client.post("/security_reports/", json={**VALID_PAYLOAD, "text": ""})
    assert response.status_code == 422


def test_create_invalid_category_returns_422(client: TestClient) -> None:
    response = client.post("/security_reports/", json={**VALID_PAYLOAD, "category": "inexistente"})
    assert response.status_code == 422


def test_get_by_id_returns_200(client: TestClient) -> None:
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    response = client.get(f"/security_reports/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_not_found_returns_404(client: TestClient) -> None:
    assert client.get("/security_reports/nonexistent").status_code == 404


def test_list_returns_200(client: TestClient) -> None:
    client.post("/security_reports/", json=VALID_PAYLOAD)
    client.post("/security_reports/", json=VALID_PAYLOAD)
    response = client.get("/security_reports/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_filter_by_category(client: TestClient) -> None:
    client.post("/security_reports/", json=VALID_PAYLOAD)
    client.post("/security_reports/", json={**VALID_PAYLOAD, "category": "transito", "text": "Semáforo quebrado"})
    response = client.get("/security_reports/?category=iluminacao")
    assert response.status_code == 200
    assert all(r["category"] == "iluminacao" for r in response.json())


def test_patch_status_returns_200(client: TestClient) -> None:
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    response = client.patch(f"/security_reports/{created['id']}/status", json={"status": "em_analise"})
    assert response.status_code == 200
    assert response.json()["status"] == "em_analise"


def test_patch_status_invalid_returns_422(client: TestClient) -> None:
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    response = client.patch(f"/security_reports/{created['id']}/status", json={"status": "inexistente"})
    assert response.status_code == 422


def test_geojson_returns_feature_collection(client: TestClient) -> None:
    client.post("/security_reports/", json=VALID_PAYLOAD)
    response = client.get("/security_reports/geojson")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 1
    feat = data["features"][0]
    assert feat["type"] == "Feature"
    assert feat["geometry"]["type"] == "Point"
    assert feat["properties"]["category"] == "iluminacao"


def test_delete_returns_204(client: TestClient) -> None:
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    assert client.delete(f"/security_reports/{created['id']}").status_code == 204


def test_delete_not_found_returns_404(client: TestClient) -> None:
    assert client.delete("/security_reports/ghost").status_code == 404


def test_patch_category_returns_200(client: TestClient) -> None:
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    response = client.patch(f"/security_reports/{created['id']}/category", json={"category": "furto_roubo"})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "furto_roubo"
    assert data["ai_suggested_category"] is None


def test_patch_category_invalid_returns_422(client: TestClient) -> None:
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    response = client.patch(f"/security_reports/{created['id']}/category", json={"category": "categoria_invalida"})
    assert response.status_code == 422


def test_patch_category_not_found_returns_404(client: TestClient) -> None:
    response = client.patch("/security_reports/nonexistent/category", json={"category": "furto_roubo"})
    assert response.status_code == 404


def test_post_auto_categorize_no_ollama(client: TestClient) -> None:
    from unittest.mock import patch
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    with patch("fala_gavea_seguranca.application.use_cases.auto_categorize_report.chat_completion",
               side_effect=RuntimeError("Ollama não está acessível")):
        response = client.post(f"/security_reports/{created['id']}/auto_categorize")
    assert response.status_code == 502


def test_post_auto_categorize_not_found_returns_404(client: TestClient) -> None:
    from unittest.mock import patch
    with patch("fala_gavea_seguranca.application.use_cases.auto_categorize_report.chat_completion"):
        response = client.post("/security_reports/nonexistent/auto_categorize")
    assert response.status_code == 404


def test_geojson_until_filter(client: TestClient, repo, db_session) -> None:
    from datetime import datetime, timezone
    from fala_gavea_seguranca.domain.entities.security_report import ReportCategory, ReportStatus, SecurityReport

    old_report = SecurityReport(
        id="old-report",
        text="Relato antigo para filtro until",
        category=ReportCategory.ILUMINACAO,
        status=ReportStatus.PENDENTE,
        author_id="user-1",
        created_at=datetime(2026, 1, 15, tzinfo=timezone.utc),
        lat=-22.9756,
        lon=-43.2296,
    )
    new_report = SecurityReport(
        id="new-report",
        text="Relato recente para filtro until",
        category=ReportCategory.ILUMINACAO,
        status=ReportStatus.PENDENTE,
        author_id="user-1",
        created_at=datetime(2026, 6, 15, tzinfo=timezone.utc),
        lat=-22.9756,
        lon=-43.2296,
    )
    repo.save(old_report)
    repo.save(new_report)

    response = client.get("/security_reports/geojson?until=2026-03-01T00:00:00")
    assert response.status_code == 200
    data = response.json()
    ids = [f["properties"]["id"] for f in data["features"]]
    assert "old-report" in ids
    assert "new-report" not in ids


def test_patch_tags(client: TestClient) -> None:
    created = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    response = client.patch(
        f"/security_reports/{created['id']}/tags",
        json={"tags": ["urgente", "verificado"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["urgente", "verificado"]


def test_get_geojson_filter_tag(client: TestClient) -> None:
    r1 = client.post("/security_reports/", json=VALID_PAYLOAD).json()
    r2 = client.post("/security_reports/", json={**VALID_PAYLOAD, "text": "Buraco na calçada da Gávea"}).json()

    client.patch(f"/security_reports/{r1['id']}/tags", json={"tags": ["urgente"]})
    client.patch(f"/security_reports/{r2['id']}/tags", json={"tags": ["resolvido"]})

    response = client.get("/security_reports/geojson?tag=urgente")
    assert response.status_code == 200
    data = response.json()
    ids = [f["properties"]["id"] for f in data["features"]]
    assert r1["id"] in ids
    assert r2["id"] not in ids
