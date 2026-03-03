from unittest.mock import patch


# -------------------------
# GET /users/{user_id}/wishlist/sets
# -------------------------


def test_get_wishlist_sets_empty(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.get_sets.return_value = []

        resp = client.get("/users/1/wishlist/sets")

    assert resp.status_code == 200
    assert resp.json() == []


def test_get_wishlist_sets_with_items(client, mock_duck):
    mock_duck.execute.return_value.fetchall.return_value = [
        ("1234-1", "Château", 2023, 100, "http://img.jpg")
    ]

    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.get_sets.return_value = [
            {"set_num": "1234-1", "priority": 1}
        ]

        resp = client.get("/users/1/wishlist/sets")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


# -------------------------
# POST /users/{user_id}/wishlist/sets
# -------------------------


def test_add_wishlist_set_success(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.add_set.return_value = {
            "set_num": "1234-1",
            "priority": 0,
        }

        resp = client.post("/users/1/wishlist/sets", json={"set_num": "1234-1"})

    assert resp.status_code == 201


def test_add_wishlist_set_duplicate(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.add_set.return_value = None

        resp = client.post("/users/1/wishlist/sets", json={"set_num": "1234-1"})

    assert resp.status_code == 409


# -------------------------
# DELETE /users/{user_id}/wishlist/sets/{set_num}
# -------------------------


def test_remove_wishlist_set_success(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.remove_set.return_value = True

        resp = client.delete("/users/1/wishlist/sets/1234-1")

    assert resp.status_code == 204


def test_remove_wishlist_set_not_found(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.remove_set.return_value = False

        resp = client.delete("/users/1/wishlist/sets/9999-1")

    assert resp.status_code == 404


# -------------------------
# GET /users/{user_id}/wishlist/parts
# -------------------------


def test_get_wishlist_parts_empty(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.get_parts.return_value = []

        resp = client.get("/users/1/wishlist/parts")

    assert resp.status_code == 200
    assert resp.json() == []


def test_get_wishlist_parts_with_items(client, mock_duck):
    mock_duck.execute.return_value.fetchall.return_value = [
        ("3001", "Brique", "http://img.jpg")
    ]

    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.get_parts.return_value = [
            {"part_num": "3001", "color_id": 4, "quantity": 1}
        ]

        resp = client.get("/users/1/wishlist/parts")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


# -------------------------
# POST /users/{user_id}/wishlist/parts
# -------------------------


def test_add_wishlist_part(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.add_part.return_value = {
            "part_num": "3001",
            "quantity": 1,
        }

        resp = client.post(
            "/users/1/wishlist/parts",
            json={"part_num": "3001", "color_id": 4, "quantity": 1},
        )

    assert resp.status_code == 201


# -------------------------
# DELETE /users/{user_id}/wishlist/parts/{part_num}/{color_id}
# -------------------------


def test_remove_wishlist_part_success(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.remove_part.return_value = True

        resp = client.delete("/users/1/wishlist/parts/3001/4")

    assert resp.status_code == 204


def test_remove_wishlist_part_not_found(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.remove_part.return_value = False

        resp = client.delete("/users/1/wishlist/parts/9999/4")

    assert resp.status_code == 404


# -------------------------
# PUT /users/{user_id}/wishlist/parts/{part_num}/{color_id}
# -------------------------


def test_update_wishlist_part_success(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.update_part_quantity.return_value = True

        resp = client.put("/users/1/wishlist/parts/3001/4", json={"quantity": 3})

    assert resp.status_code == 200
    assert resp.json()["quantity"] == 3


def test_update_wishlist_part_not_found(client):
    with patch("app.controller.wishlist_controller.WishlistService") as mock_svc:
        mock_svc.return_value.update_part_quantity.return_value = False

        resp = client.put("/users/1/wishlist/parts/9999/4", json={"quantity": 3})

    assert resp.status_code == 404
