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
        user = self.dao.get_by_username(username)
        if user is None:
            raise Exception(f"Utilisateur '{username}' introuvable")
        if hash_password(password, user.salt) != user.hashed_password:
            raise Exception("Mot de passe incorrect")
        return user
