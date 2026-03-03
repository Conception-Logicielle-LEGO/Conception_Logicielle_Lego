from unittest.mock import MagicMock, patch

from app.business_object.user import User


def _fake_user(username="john", id_user=1):
    u = User(username=username, hashed_password="hash", salt="salt")
    u.id_user = id_user
    return u


# -------------------------
# POST /users  (register)
# -------------------------


def test_register_success(client):
    with (
        patch("app.controller.user_controller.UserDAO") as mock_dao_cls,
        patch("app.controller.user_controller.UserService") as mock_service_cls,
    ):
        mock_dao = MagicMock()
        mock_dao_cls.return_value = mock_dao
        mock_dao.is_username_taken.return_value = False
        mock_service_cls.return_value.create_user.return_value = _fake_user()

        resp = client.post("/users", json={"username": "john", "password": "pass"})

    assert resp.status_code == 201
    assert resp.json()["username"] == "john"


def test_register_username_taken(client):
    with patch("app.controller.user_controller.UserDAO") as mock_dao_cls:
        mock_dao_cls.return_value.is_username_taken.return_value = True

        resp = client.post("/users", json={"username": "john", "password": "pass"})

    assert resp.status_code == 409


def test_register_creation_fails(client):
    with (
        patch("app.controller.user_controller.UserDAO") as mock_dao_cls,
        patch("app.controller.user_controller.UserService") as mock_service_cls,
    ):
        mock_dao_cls.return_value.is_username_taken.return_value = False
        mock_service_cls.return_value.create_user.return_value = None

        resp = client.post("/users", json={"username": "john", "password": "pass"})

    assert resp.status_code == 500


# -------------------------
# POST /users/login
# -------------------------


def test_login_success(client):
    with (
        patch("app.controller.user_controller.UserDAO"),
        patch("app.controller.user_controller.PasswordService") as mock_ps_cls,
    ):
        mock_ps_cls.return_value.validate_username_password.return_value = _fake_user()

        resp = client.post("/users/login", json={"username": "john", "password": "pass"})

    assert resp.status_code == 200
    assert resp.json()["id_user"] == 1


def test_login_wrong_password(client):
    with (
        patch("app.controller.user_controller.UserDAO"),
        patch("app.controller.user_controller.PasswordService") as mock_ps_cls,
    ):
        mock_ps_cls.return_value.validate_username_password.side_effect = Exception(
            "Mot de passe incorrect"
        )

        resp = client.post("/users/login", json={"username": "john", "password": "wrong"})

    assert resp.status_code == 401


# -------------------------
# PUT /users/{user_id}/password
# -------------------------


def test_change_password_success(client):
    with (
        patch("app.controller.user_controller.UserDAO") as mock_dao_cls,
        patch("app.controller.user_controller.UserService") as mock_service_cls,
    ):
        mock_dao_cls.return_value.get_by_id.return_value = _fake_user()
        mock_service_cls.return_value.change_password.return_value = True

        resp = client.put(
            "/users/1/password", json={"old_password": "old", "new_password": "new"}
        )

    assert resp.status_code == 200


def test_change_password_user_not_found(client):
    with patch("app.controller.user_controller.UserDAO") as mock_dao_cls:
        mock_dao_cls.return_value.get_by_id.return_value = None

        resp = client.put(
            "/users/1/password", json={"old_password": "old", "new_password": "new"}
        )

    assert resp.status_code == 404


def test_change_password_wrong_old(client):
    with (
        patch("app.controller.user_controller.UserDAO") as mock_dao_cls,
        patch("app.controller.user_controller.UserService") as mock_service_cls,
    ):
        mock_dao_cls.return_value.get_by_id.return_value = _fake_user()
        mock_service_cls.return_value.change_password.return_value = False

        resp = client.put(
            "/users/1/password", json={"old_password": "wrong", "new_password": "new"}
        )

    assert resp.status_code == 400


# -------------------------
# PUT /users/{user_id}/username
# -------------------------


def test_change_username_success(client):
    with (
        patch("app.controller.user_controller.UserDAO") as mock_dao_cls,
        patch("app.controller.user_controller.UserService") as mock_service_cls,
    ):
        mock_dao_cls.return_value.get_by_id.return_value = _fake_user()
        mock_service_cls.return_value.change_username.return_value = True

        resp = client.put("/users/1/username", json={"new_username": "newjohn"})

    assert resp.status_code == 200


def test_change_username_user_not_found(client):
    with patch("app.controller.user_controller.UserDAO") as mock_dao_cls:
        mock_dao_cls.return_value.get_by_id.return_value = None

        resp = client.put("/users/1/username", json={"new_username": "newjohn"})

    assert resp.status_code == 404


def test_change_username_taken(client):
    with (
        patch("app.controller.user_controller.UserDAO") as mock_dao_cls,
        patch("app.controller.user_controller.UserService") as mock_service_cls,
    ):
        mock_dao_cls.return_value.get_by_id.return_value = _fake_user()
        mock_service_cls.return_value.change_username.return_value = False

        resp = client.put("/users/1/username", json={"new_username": "taken"})

    assert resp.status_code == 409
