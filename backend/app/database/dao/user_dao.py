from app.business_object.user import User
from app.database.dao.base_dao import BaseDAO


class UserDAO(BaseDAO):
    """
    DAO pour gérer les utilisateurs dans la base de données.
    Hérite de BaseDAO pour bénéficier des méthodes génériques.
    """

    def get_table_name(self) -> str:
        return "users"

    def get_allowed_columns(self) -> set[str]:
        return {"username", "id_user"}

    def from_row(self, row: dict) -> User:
        """Convertit une ligne SQL en objet User"""
        return User.from_dict(row)

    def create_user(self, user: User) -> User | None:
        """
        Créer un nouvel utilisateur dans la base de données

        Paramètres :
        ------------
        user : User
            Utilisateur de type User sans id_user

        Renvoie :
        ---------
        User | None :
            Un objet de type User avec l'id_user créé par la BDD,
            ou None en cas d'erreur
        """
        with self.conn as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO users (username, password, salt) VALUES (?, ?, ?)
                    RETURNING id_user
                """,
                    [user.username, user.password, user.salt],
                )
                id_user = cursor.fetchone()[0]
                return User(
                    username=user.username,
                    password=user.password,
                    id_user=id_user,
                    salt=user.salt,
                )
            except Exception as e:
                print(f"Error creating user: {e}")
                return None

    def delete_user(self, id_user: int) -> bool:
        """
        Supprime un utilisateur à partir de son id_user

        Paramètre :
        -----------
        id_user : int
            ID de l'utilisateur à supprimer

        Renvoie :
        ---------
        bool :
            True si succès, False si échec
        """
        try:
            self.conn.execute("DELETE FROM users WHERE id_user = ?", [id_user])
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def update_user(self, update_username: bool, new_entry: str, id_user: int) -> bool:
        """
        DAO pour changer soit le username soit le mot de passe d'un utilisateur connecté

        Paramètres :
        ------------
        update_username : bool
            True pour mettre à jour le username, False pour le mot de passe
        new_entry : str
            Nouvelle entrée (nouveau username ou mot de passe déjà hashé)
        id_user : int
            ID de l'utilisateur

        Renvoie :
        ---------
        bool :
            True si succès, False si échec
        """
        if update_username:
            result = self.conn.execute(
                """
                UPDATE users
                SET username = ?
                WHERE id_user = ?
                RETURNING id_user;""",
                [new_entry, id_user],
            ).fetchone()
        else:
            result = self.conn.execute(
                """
                UPDATE users
                SET password = ?
                WHERE id_user = ?
                RETURNING id_user;""",
                [new_entry, id_user],
            ).fetchone()
        return result is not None

    def is_username_taken(self, username: str) -> bool:
        """
        Vérifie si un username est déjà utilisé.
        Utile pour assurer l'unicité des usernames lors de l'inscription
        ou modification de profil des utilisateurs.

        Paramètre :
        -----------
        username : str
            Nom d'utilisateur à tester

        Renvoie :
        ---------
        bool :
            True si le nom est occupé, False s'il est libre

        Note :
        ------
        Utilise la méthode exists() héritée de BaseDAO
        """
        return self.exists("username", username)
