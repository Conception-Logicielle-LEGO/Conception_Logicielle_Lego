from business_object.user import User
from database.dao.user_dao import UserDAO
from service.password_service import create_salt, validate_username_password
from utils.securite import hash_password


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao or UserDAO()

    def create_user(self, username, password):
        """
        Créer un nouvel utilisateur avec son username et le password non hashé
        Génère un salt, hash le mot de passe avec, stocke tout dans un objet user puis l'ajoute à la bdd

        Paramètres :
        username : str nom de l'utilisateur
        password : str mot de passe entré par l'utilisateur

        Renvoie :
        user : User complet avec l'id_user attribué par la table, le mot de passe hashé et le salt
        """
        salt = create_salt()
        hashed_password = hash_password(password)

        new_user = User(
            username=username,
            password=hashed_password,
            salt=salt,
        )

        return self.create_user(new_user)

    def change_password(self, username, old_password, new_password):
        """
        Change le mot de passe de l'utilisateur après avoir vérifié que l'ancien mot de passe était bon

        Paramètres :
        username : str
        old_password : str
        new_password : str

        Renvoie :
        Bool : False si la fonction échoue, True si elle réussit"""
        user = validate_username_password(
            username=username, password=old_password, user_dao=self.user_dao
        )
        if user is None:
            return False

        # Faut il refaire un salt ?
        hashed_password = hash_password(password=new_password, sel=user.salt)

        return self.user_dao.update_user(
            update_username=False, new_entry=hashed_password, id_user=user.id_user
        )

    def change_username(self, username, new_username):
        """
        Change le nom d'utilisateur pour un nouveau nom si ce dernier n'est pas déjà utilisé par quelqu'un
        Paramètres :
        username : str
        new_username : str

        Renvoie:
        False si échec True si succès"""

        new_username_ok = self.user_dao.is_username_taken(new_username)
        if new_username_ok:
            return False

        else:
            user = self.user_dao.get_user(username=username)

            return self.user_dao.update_user(
                update_username=True, new_entry=new_username, id_user=user.id_user
            )
