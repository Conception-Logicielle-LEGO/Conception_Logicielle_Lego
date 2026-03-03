from unittest.mock import MagicMock, patch

from app.business_object.user_owned_set import UserOwnedSet


def _fake_set(set_num="1234-1", is_built=False):
    s = UserOwnedSet(id_user=1, set_num=set_num, is_built=is_built)
    return s


# -------------------------
# GET /users/{user_id}/collection
# -------------------------


def test_get_collection_empty(client):
    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.get_collection.return_value = []

        resp = client.get("/users/1/collection")

    assert resp.status_code == 200
    assert resp.json() == []


def test_get_collection_with_sets(client, mock_duck):
    fake = _fake_set("1234-1")
    mock_duck.execute.return_value.fetchall.return_value = [
        ("1234-1", "Château", 2023, 100, "http://img.jpg")
    ]

    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.get_collection.return_value = [fake]

        resp = client.get("/users/1/collection")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


# -------------------------
# POST /users/{user_id}/collection
# -------------------------


def test_add_to_collection_success(client):
    fake = _fake_set("1234-1")

    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.add_set.return_value = fake

        resp = client.post("/users/1/collection", json={"set_num": "1234-1"})

    assert resp.status_code == 201


def test_add_to_collection_duplicate(client):
    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.add_set.return_value = None

        resp = client.post("/users/1/collection", json={"set_num": "1234-1"})

    assert resp.status_code == 409


# -------------------------
# DELETE /users/{user_id}/collection/{set_num}
# -------------------------


def test_remove_from_collection_success(client):
    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.remove_set.return_value = True

        resp = client.delete("/users/1/collection/1234-1")

    assert resp.status_code == 204


def test_remove_from_collection_not_found(client):
    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.remove_set.return_value = False

        resp = client.delete("/users/1/collection/9999-1")

    assert resp.status_code == 404


# -------------------------
# PUT /users/{user_id}/collection/{set_num}/built
# -------------------------


def test_update_built_status_success(client):
    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.mark_built.return_value = True

        resp = client.put("/users/1/collection/1234-1/built", json={"is_built": True})

    assert resp.status_code == 200
    assert resp.json()["is_built"] is True


def test_update_built_status_not_found(client):
    with patch("app.controller.collection_controller.CollectionService") as mock_svc:
        mock_svc.return_value.mark_built.return_value = False

        resp = client.put("/users/1/collection/9999-1/built", json={"is_built": True})

    assert resp.status_code == 404
