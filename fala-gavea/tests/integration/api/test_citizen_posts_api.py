import pytest
from fastapi.testclient import TestClient

VALID_PAYLOAD = {
    "text": "Precisa de mais iluminação na rua principal",
    "territory_level": "neighborhood",
    "territory_name": "Gávea",
    "author_id": "user-abc",
}


def test_create_citizen_post_returns_201(client: TestClient) -> None:
    response = client.post("/citizen_posts/", json=VALID_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == VALID_PAYLOAD["text"]
    assert data["territory_level"] == "neighborhood"
    assert "id" in data
    assert "created_at" in data


def test_create_citizen_post_empty_text_returns_422(client: TestClient) -> None:
    payload = {**VALID_PAYLOAD, "text": ""}
    response = client.post("/citizen_posts/", json=payload)
    assert response.status_code == 422


def test_create_citizen_post_short_text_returns_422(client: TestClient) -> None:
    payload = {**VALID_PAYLOAD, "text": "Hi"}
    response = client.post("/citizen_posts/", json=payload)
    assert response.status_code == 422


def test_get_citizen_post_by_id_returns_200(client: TestClient) -> None:
    created = client.post("/citizen_posts/", json=VALID_PAYLOAD).json()
    response = client.get(f"/citizen_posts/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_citizen_post_not_found_returns_404(client: TestClient) -> None:
    response = client.get("/citizen_posts/nonexistent-id")
    assert response.status_code == 404


def test_list_citizen_posts_returns_200(client: TestClient) -> None:
    client.post("/citizen_posts/", json=VALID_PAYLOAD)
    client.post("/citizen_posts/", json=VALID_PAYLOAD)
    response = client.get("/citizen_posts/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_citizen_post_returns_204(client: TestClient) -> None:
    created = client.post("/citizen_posts/", json=VALID_PAYLOAD).json()
    response = client.delete(f"/citizen_posts/{created['id']}")
    assert response.status_code == 204


def test_delete_citizen_post_not_found_returns_404(client: TestClient) -> None:
    response = client.delete("/citizen_posts/ghost-id")
    assert response.status_code == 404
