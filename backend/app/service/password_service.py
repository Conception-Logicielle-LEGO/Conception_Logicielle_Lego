import secrets

from app.business_object.user import User
from app.database.dao.user_dao import UserDAO
from app.utils.securite import hash_password


class PasswordService:
    def __init__(self, user_dao: UserDAO):
        self.dao = user_dao

    def create_salt(self) -> str:
        """Génère un sel aléatoire de 256 caractères hexadécimaux."""
        return secrets.token_hex(128)

    def validate_username_password(self, username: str, password: str) -> User:
        """
        Vérifie que le mot de passe est correct pour un utilisateur donné.

        Renvoie :
        ---------
        User : l'utilisateur si les identifiants sont valides

        Lève :
        ------
        Exception si l'utilisateur est introuvable ou le mot de passe incorrect
        """
        user_with_username = self.dao.get_user(username=username)
        if user_with_username is None:
            raise Exception(f"user with username {username} not found")

        salt = user_with_username.salt
        stored_hash = user_with_username.hashed_password

        computed_hash = hash_password(password, salt)

        if computed_hash != stored_hash:
            raise Exception("Incorrect password")

        return user_with_username
