import pytest
from unittest.mock import MagicMock, patch

from app.service.user_service import UserService
from app.business_object.user import User


# -------------------------
# Test create_user
# -------------------------

def test_create_user_success():
    mock_dao = MagicMock()

    created_user = User(username="john", hashed_password="hashednewpass", salt="randomsalt")
    created_user.id_user = 42
    mock_dao.create_user.return_value = created_user

    with patch("app.service.user_service.PasswordService") as MockPasswordService, \
         patch("app.service.user_service.hash_password", return_value="hashednewpass"):
        instance = MockPasswordService.return_value
        instance.create_salt.return_value = "randomsalt"

        service = UserService(user_dao=mock_dao)
        result = service.create_user(username="john", password="plainpass")

        mock_dao.create_user.assert_called_once()
        assert result.id_user == 42
        assert result.username == "john"


# -------------------------
# Test change_password
# -------------------------

def test_change_password_success():
    # Mock DAO
    mock_dao = MagicMock()

    # Fake user retourné par validate_username_password
    fake_user = User(username="john", hashed_password="oldhash", salt="salt123")
    fake_user.id_user = 1

    # Mock PasswordService
    with patch("app.service.user_service.PasswordService") as MockPasswordService:
        instance = MockPasswordService.return_value
        instance.validate_username_password.return_value = fake_user

        mock_dao.update_user.return_value = True

        service = UserService(user_dao=mock_dao)

        result = service.change_password(
            username="john",
            old_password="oldpass",
            new_password="newpass"
        )

        assert result is True
        mock_dao.update_user.assert_called_once()


def test_change_password_wrong_old_password():
    mock_dao = MagicMock()

    with patch("app.service.user_service.PasswordService") as MockPasswordService:
        instance = MockPasswordService.return_value
        instance.validate_username_password.return_value = None

        service = UserService(user_dao=mock_dao)

        result = service.change_password(
            username="john",
            old_password="wrongpass",
            new_password="newpass"
        )

        assert result is False
        mock_dao.update_user.assert_not_called()


# -------------------------
# Test change_username
# -------------------------

def test_change_username_success():
    mock_dao = MagicMock()

    fake_user = User(username="john", hashed_password="hash", salt="salt")
    fake_user.id_user = 1

    mock_dao.is_username_taken.return_value = False
    mock_dao.get_user.return_value = fake_user
    mock_dao.update_user.return_value = True

    service = UserService(user_dao=mock_dao)

    result = service.change_username("john", "newjohn")

    assert result is True
    mock_dao.update_user.assert_called_once()


def test_change_username_already_taken():
    mock_dao = MagicMock()
    mock_dao.is_username_taken.return_value = True

    service = UserService(user_dao=mock_dao)

    result = service.change_username("john", "newjohn")

    assert result is False
    mock_dao.update_user.assert_not_called()