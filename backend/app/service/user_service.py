from app.business_object.user import User
from app.database.dao.user_dao import UserDAO
from app.service.password_service import PasswordService
from app.utils.securite import hash_password


class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def create_user(self, username: str, password: str) -> User | None:
        """
        Crée un nouvel utilisateur avec son mot de passe hashé et un sel.

        Renvoie :
        ---------
        User | None : l'utilisateur créé avec son id_user, ou None en cas d'erreur
        """
        passwordservice = PasswordService(user_dao=self.user_dao)
        salt = passwordservice.create_salt()
        hashed_password = hash_password(password)

        new_user = User(
            username=username,
            hashed_password=hashed_password,
            salt=salt,
        )

        return self.user_dao.create_user(new_user)

    def change_password(
        self, username: str, old_password: str, new_password: str
    ) -> bool:
        """
        Change le mot de passe après validation de l'ancien.

        Renvoie :
        ---------
        bool : True si succès, False si échec
        """
        password_service = PasswordService(user_dao=self.user_dao)
        try:
            user = password_service.validate_username_password(username, old_password)
        except Exception:
            return False
        hashed = hash_password(new_password, user.salt)
        return self.user_dao.update_user(
            update_username=False, new_entry=hashed, id_user=user.id_user
        )

    def change_username(self, username: str, new_username: str) -> bool:
        """
        Change le nom d'utilisateur si le nouveau n'est pas déjà pris.

        Renvoie :
        ---------
        bool : True si succès, False si le nouveau username est déjà pris ou user introuvable
        """
        if self.user_dao.is_username_taken(new_username):
            return False
        user = self.user_dao.get_by_username(username)
        if user is None:
            return False
        return self.user_dao.update_user(
            update_username=True, new_entry=new_username, id_user=user.id_user
        )
