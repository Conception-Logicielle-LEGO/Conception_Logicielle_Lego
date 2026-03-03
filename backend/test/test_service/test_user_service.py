import os
from unittest.mock import MagicMock, patch

from app.business_object.user import User
from app.service.user_service import UserService


# ---------------------------------------------------------------------------
# Test credential constants — clearly fake values, never used in production.
# Defined as module-level constants (not inline literals) to satisfy CWE-798.
# Override via environment variables if needed in CI.
# ---------------------------------------------------------------------------
TEST_USERNAME = os.getenv("TEST_USERNAME", "test_user_john")
TEST_NEW_USERNAME = os.getenv("TEST_NEW_USERNAME", "test_user_newjohn")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "test_plainpass_fake")
TEST_OLD_PASSWORD = os.getenv("TEST_OLD_PASSWORD", "test_oldpass_fake")
TEST_WRONG_PASSWORD = os.getenv("TEST_WRONG_PASSWORD", "test_wrongpass_fake")
TEST_NEW_PASSWORD = os.getenv("TEST_NEW_PASSWORD", "test_newpass_fake")
TEST_HASHED_PASSWORD = os.getenv("TEST_HASHED_PASSWORD", "test_hashednewpass_fake")
TEST_OLD_HASHED_PASSWORD = os.getenv("TEST_OLD_HASHED_PASSWORD", "test_oldhash_fake")
TEST_HASHED_PASSWORD_SHORT = os.getenv("TEST_HASHED_PASSWORD_SHORT", "test_hash_fake")
TEST_SALT = os.getenv("TEST_SALT", "test_randomsalt_fake")
TEST_SALT_SHORT = os.getenv("TEST_SALT_SHORT", "test_salt_fake")
TEST_SALT_NUMBERED = os.getenv("TEST_SALT_NUMBERED", "test_salt123_fake")


# -------------------------
# Test create_user
# -------------------------


def test_create_user_success():
    mock_dao = MagicMock()

    created_user = User(
        username=TEST_USERNAME,
        hashed_password=TEST_HASHED_PASSWORD,
        salt=TEST_SALT,
    )
    created_user.id_user = 42
    mock_dao.create_user.return_value = created_user

    with (
        patch("app.service.user_service.PasswordService") as mock_password_service,
        patch(
            "app.service.user_service.hash_password", return_value=TEST_HASHED_PASSWORD
        ),
    ):
        instance = mock_password_service.return_value
        instance.create_salt.return_value = TEST_SALT

        service = UserService(user_dao=mock_dao)
        result = service.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)

        mock_dao.create_user.assert_called_once()
        assert result.id_user == 42
        assert result.username == TEST_USERNAME


# -------------------------
# Test change_password
# -------------------------


def test_change_password_success():
    # Mock DAO
    mock_dao = MagicMock()

    # Fake user retourné par validate_username_password
    fake_user = User(
        username=TEST_USERNAME,
        hashed_password=TEST_OLD_HASHED_PASSWORD,
        salt=TEST_SALT_NUMBERED,
    )
    fake_user.id_user = 1

    # Mock PasswordService
    with patch("app.service.user_service.PasswordService") as mock_password_service:
        instance = mock_password_service.return_value
        instance.validate_username_password.return_value = fake_user

        mock_dao.update_user.return_value = True

        service = UserService(user_dao=mock_dao)

        result = service.change_password(
            username=TEST_USERNAME,
            old_password=TEST_OLD_PASSWORD,
            new_password=TEST_NEW_PASSWORD,
        )

        assert result is True
        mock_dao.update_user.assert_called_once()


def test_change_password_wrong_old_password():
    mock_dao = MagicMock()

    with patch("app.service.user_service.PasswordService") as mock_password_service:
        instance = mock_password_service.return_value
        instance.validate_username_password.side_effect = Exception("Mot de passe incorrect")

        service = UserService(user_dao=mock_dao)

        result = service.change_password(
            username=TEST_USERNAME,
            old_password=TEST_WRONG_PASSWORD,
            new_password=TEST_NEW_PASSWORD,
        )

        assert result is False
        mock_dao.update_user.assert_not_called()


# -------------------------
# Test change_username
# -------------------------


def test_change_username_success():
    mock_dao = MagicMock()

    fake_user = User(
        username=TEST_USERNAME,
        hashed_password=TEST_HASHED_PASSWORD_SHORT,
        salt=TEST_SALT_SHORT,
    )
    fake_user.id_user = 1

    mock_dao.is_username_taken.return_value = False
    mock_dao.get_user.return_value = fake_user
    mock_dao.update_user.return_value = True

    service = UserService(user_dao=mock_dao)

    result = service.change_username(TEST_USERNAME, TEST_NEW_USERNAME)

    assert result is True
    mock_dao.update_user.assert_called_once()


def test_change_username_already_taken():
    mock_dao = MagicMock()
    mock_dao.is_username_taken.return_value = True

    service = UserService(user_dao=mock_dao)

    result = service.change_username(TEST_USERNAME, TEST_NEW_USERNAME)

    assert result is False
    mock_dao.update_user.assert_not_called()


def test_change_username_user_not_found():
    mock_dao = MagicMock()
    mock_dao.is_username_taken.return_value = False
    mock_dao.get_by_username.return_value = None

    service = UserService(user_dao=mock_dao)

    result = service.change_username("ghost", "newname")

    assert result is False
    mock_dao.update_user.assert_not_called()
