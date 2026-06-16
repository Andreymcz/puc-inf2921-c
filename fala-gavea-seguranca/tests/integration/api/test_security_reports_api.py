import pytest
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
