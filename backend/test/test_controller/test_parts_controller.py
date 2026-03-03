from unittest.mock import patch


# -------------------------
# GET /users/{user_id}/parts
# -------------------------


def test_get_owned_parts_empty(client):
    with patch("app.controller.parts_controller.UserPartsService") as mock_svc:
        mock_svc.return_value.get_owned_parts.return_value = []

        resp = client.get("/users/1/parts")

    assert resp.status_code == 200
    assert resp.json() == []


def test_get_owned_parts_with_items(client, mock_duck):
    mock_duck.execute.return_value.fetchall.return_value = [
        ("3001", "Brique", "http://img.jpg")
    ]

    with patch("app.controller.parts_controller.UserPartsService") as mock_svc:
        mock_svc.return_value.get_owned_parts.return_value = [
            {"part_num": "3001", "color_id": 4, "quantity": 2}
        ]

        resp = client.get("/users/1/parts")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


# -------------------------
# POST /users/{user_id}/parts
# -------------------------


def test_add_owned_part(client):
    with patch("app.controller.parts_controller.UserPartsService") as mock_svc:
        mock_svc.return_value.add_part.return_value = {
            "part_num": "3001",
            "quantity": 2,
        }

        resp = client.post(
            "/users/1/parts", json={"part_num": "3001", "color_id": 4, "quantity": 2}
        )

    assert resp.status_code == 201


# -------------------------
# DELETE /users/{user_id}/parts/{part_num}/{color_id}
# -------------------------


def test_remove_owned_part_success(client):
    with patch("app.controller.parts_controller.UserPartsService") as mock_svc:
        mock_svc.return_value.remove_part.return_value = True

        resp = client.delete("/users/1/parts/3001/4")

    assert resp.status_code == 204


def test_remove_owned_part_not_found(client):
    with patch("app.controller.parts_controller.UserPartsService") as mock_svc:
        mock_svc.return_value.remove_part.return_value = False

        resp = client.delete("/users/1/parts/9999/4")

    assert resp.status_code == 404


# -------------------------
# PUT /users/{user_id}/parts/{part_num}/{color_id}
# -------------------------


def test_update_owned_part_quantity_success(client):
    with patch("app.controller.parts_controller.UserPartsService") as mock_svc:
        mock_svc.return_value.update_quantity.return_value = True

        resp = client.put("/users/1/parts/3001/4", json={"quantity": 5})

    assert resp.status_code == 200
    assert resp.json()["quantity"] == 5


def test_update_owned_part_quantity_not_found(client):
    with patch("app.controller.parts_controller.UserPartsService") as mock_svc:
        mock_svc.return_value.update_quantity.return_value = False

        resp = client.put("/users/1/parts/9999/4", json={"quantity": 5})

    assert resp.status_code == 404
