from unittest.mock import patch

from app.business_object.favorite_set import FavoriteSet


def _fake_fav(set_num="1234-1"):
    return FavoriteSet(id_user=1, set_num=set_num)


# -------------------------
# GET /users/{user_id}/favorites
# -------------------------


def test_get_favorites_empty(client):
    with patch("app.controller.favorites_controller.FavoriteService") as mock_svc:
        mock_svc.return_value.get_favorites.return_value = []

        resp = client.get("/users/1/favorites")

    assert resp.status_code == 200
    assert resp.json() == []


def test_get_favorites_with_items(client, mock_duck):
    mock_duck.execute.return_value.fetchall.return_value = [
        ("1234-1", "Château", 2023, 100, "http://img.jpg")
    ]

    with patch("app.controller.favorites_controller.FavoriteService") as mock_svc:
        mock_svc.return_value.get_favorites.return_value = [_fake_fav()]

        resp = client.get("/users/1/favorites")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


# -------------------------
# POST /users/{user_id}/favorites
# -------------------------


def test_add_favorite_success(client):
    with patch("app.controller.favorites_controller.FavoriteService") as mock_svc:
        mock_svc.return_value.add_favorite.return_value = _fake_fav()

        resp = client.post("/users/1/favorites", json={"set_num": "1234-1"})

    assert resp.status_code == 201


def test_add_favorite_duplicate(client):
    with patch("app.controller.favorites_controller.FavoriteService") as mock_svc:
        mock_svc.return_value.add_favorite.return_value = None

        resp = client.post("/users/1/favorites", json={"set_num": "1234-1"})

    assert resp.status_code == 409


# -------------------------
# DELETE /users/{user_id}/favorites/{set_num}
# -------------------------


def test_remove_favorite_success(client):
    with patch("app.controller.favorites_controller.FavoriteService") as mock_svc:
        mock_svc.return_value.remove_favorite.return_value = True

        resp = client.delete("/users/1/favorites/1234-1")

    assert resp.status_code == 204


def test_remove_favorite_not_found(client):
    with patch("app.controller.favorites_controller.FavoriteService") as mock_svc:
        mock_svc.return_value.remove_favorite.return_value = False

        resp = client.delete("/users/1/favorites/9999-1")

    assert resp.status_code == 404
