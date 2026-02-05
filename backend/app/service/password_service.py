import secrets

from business_object.user import User
from database.dao.user_dao import UserDAO
from utils.securite import hash_password


def create_salt() -> str:
    return secrets.token_hex(128)


def validate_username_password(username: str, password: str, user_dao: UserDAO) -> User:
    """
    Vérifie que le mot de passe entré est correct et dans ce cas renvoie le profil utilisateur complet
    """
    user_with_username = user_dao.get_user(username=username)
    if user_with_username is None:
        raise Exception(f"user with username {username} not found")

    salt = user_with_username.salt
    stored_hash = user_with_username.password

    computed_hash = hash_password(password, salt)

    if computed_hash != stored_hash:
        raise Exception("Incorrect password")

    return user_with_username
