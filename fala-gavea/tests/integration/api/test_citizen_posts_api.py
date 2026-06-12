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


def test_toggle_like_adds_like(client: TestClient) -> None:
    created = client.post("/citizen_posts/", json=VALID_PAYLOAD).json()
    response = client.post(f"/citizen_posts/{created['id']}/likes", json={"user_id": "u1"})
    assert response.status_code == 200
    data = response.json()
    assert data["liked"] is True
    assert data["likes_count"] == 1


def test_toggle_like_removes_like(client: TestClient) -> None:
    created = client.post("/citizen_posts/", json=VALID_PAYLOAD).json()
    client.post(f"/citizen_posts/{created['id']}/likes", json={"user_id": "u1"})
    response = client.post(f"/citizen_posts/{created['id']}/likes", json={"user_id": "u1"})
    assert response.status_code == 200
    data = response.json()
    assert data["liked"] is False
    assert data["likes_count"] == 0


def test_add_label_feedback(client: TestClient) -> None:
    created = client.post("/citizen_posts/", json=VALID_PAYLOAD).json()
    response = client.post(
        f"/citizen_posts/{created['id']}/label_feedback",
        json={"label": "iluminação", "approved": True, "user_id": "u1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["label_feedback"]["iluminação"]["approved"] is True
    assert data["label_feedback"]["iluminação"]["user_id"] == "u1"


def test_get_post_likes_endpoint(client: TestClient) -> None:
    created = client.post("/citizen_posts/", json=VALID_PAYLOAD).json()
    post_id = created["id"]

    # No likes yet — should return empty likers list
    response = client.get(f"/citizen_posts/{post_id}/likes")
    assert response.status_code == 200
    data = response.json()
    assert data["post_id"] == post_id
    assert data["likers"] == []

    # Add a like
    client.post(f"/citizen_posts/{post_id}/likes", json={"user_id": "u1"})
    response = client.get(f"/citizen_posts/{post_id}/likes")
    assert response.status_code == 200
    data = response.json()
    assert len(data["likers"]) == 1
    assert data["likers"][0]["user_id"] == "u1"
    assert "created_at" in data["likers"][0]


def test_get_post_likes_not_found_returns_404(client: TestClient) -> None:
    response = client.get("/citizen_posts/nonexistent-id/likes")
    assert response.status_code == 404


BULK_PAYLOAD = {
    "items": [
        {**VALID_PAYLOAD, "text": "Falta iluminação na praça central"},
        {**VALID_PAYLOAD, "text": "O transporte público precisa melhorar"},
    ]
}


def test_bulk_create_returns_201_with_all_items(client: TestClient) -> None:
    response = client.post("/citizen_posts/bulk", json=BULK_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert len(data["items"]) == 2
    for item in data["items"]:
        assert "id" in item
        assert "text" in item
        assert "created_at" in item


def test_bulk_create_empty_list_returns_201(client: TestClient) -> None:
    response = client.post("/citizen_posts/bulk", json={"items": []})
    assert response.status_code == 201
    assert response.json()["items"] == []


def test_bulk_create_invalid_item_returns_422(client: TestClient) -> None:
    payload = {"items": [{**VALID_PAYLOAD, "text": "Hi"}]}
    response = client.post("/citizen_posts/bulk", json=payload)
    assert response.status_code == 422


def test_bulk_create_posts_are_retrievable(client: TestClient) -> None:
    client.post("/citizen_posts/bulk", json=BULK_PAYLOAD)
    response = client.get("/citizen_posts/")
    assert response.status_code == 200
    assert len(response.json()) == 2
