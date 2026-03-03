from unittest.mock import MagicMock, patch

import pytest

from app.business_object.user import User
from app.service.password_service import PasswordService


# -------------------------
# Test create_salt
# -------------------------


def test_create_salt_returns_hex_string():
    service = PasswordService(user_dao=MagicMock())
    salt = service.create_salt()
    assert isinstance(salt, str)
    assert len(salt) == 256  # secrets.token_hex(128) → 128 bytes × 2 hex chars


# -------------------------
# Test validate_username_password
# -------------------------


def test_validate_username_password_success():
    dao = MagicMock()
    fake_user = User(username="john", hashed_password="correcthash", salt="somesalt")
    dao.get_user.return_value = fake_user

    with patch(
        "app.service.password_service.hash_password", return_value="correcthash"
    ):
        service = PasswordService(user_dao=dao)
        result = service.validate_username_password("john", "plainpass")
        assert result == fake_user


def test_validate_username_password_user_not_found():
    dao = MagicMock()
    dao.get_user.return_value = None

    service = PasswordService(user_dao=dao)
    with pytest.raises(Exception, match="not found"):
        service.validate_username_password("unknown", "pass")


def test_validate_username_password_wrong_password():
    dao = MagicMock()
    fake_user = User(username="john", hashed_password="correcthash", salt="somesalt")
    dao.get_user.return_value = fake_user

    with patch("app.service.password_service.hash_password", return_value="wronghash"):
        service = PasswordService(user_dao=dao)
        with pytest.raises(Exception, match="Incorrect password"):
            service.validate_username_password("john", "wrongpass")
