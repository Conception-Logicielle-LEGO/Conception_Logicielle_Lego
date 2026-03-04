import logging

from app.business_object.user import User


logger = logging.getLogger(__name__)


class UserDAO:
    """
    DAO pour gérer les utilisateurs dans la base de données PostgreSQL.
    Utilise une connexion injectée (pattern CollectionDAO/FavoriteDAO).
    Ne fait jamais commit() — la gestion des transactions est à la charge de l'appelant.
    """

    def __init__(self, pg_conn):
        self.conn = pg_conn

    def create_user(self, user: User) -> User | None:
        """
        Crée un nouvel utilisateur dans la base de données.

        Paramètres :
        ------------
        user : User
            Utilisateur sans id_user (sera attribué par la BDD)

        Renvoie :
        ---------
        User | None :
            Utilisateur avec l'id_user assigné, ou None en cas d'erreur
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (username, hashed_password, salt)
                    VALUES (%s, %s, %s)
                    RETURNING id_user
                    """,
                    [user.username, user.hashed_password, user.salt],
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return User(
                    username=user.username,
                    hashed_password=user.hashed_password,
                    salt=user.salt,
                    id_user=row["id_user"],
                )
        except Exception:
            logger.exception("Erreur création utilisateur")
            return None

    def get_by_username(self, username: str) -> User | None:
        """
        Récupère un utilisateur par son username.

        Renvoie :
        ---------
        User | None
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", [username])
            row = cur.fetchone()
            return User.from_dict(dict(row)) if row else None

    def get_by_id(self, id_user: int) -> User | None:
        """
        Récupère un utilisateur par son id_user.

        Renvoie :
        ---------
        User | None
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id_user = %s", [id_user])
            row = cur.fetchone()
            return User.from_dict(dict(row)) if row else None

    def delete_user(self, id_user: int) -> bool:
        """
        Supprime un utilisateur à partir de son id_user.

        Renvoie :
        ---------
        bool : True si succès, False si erreur
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id_user = %s", [id_user])
                return True
        except Exception:
            logger.exception("Erreur suppression utilisateur")
            return False

    def update_user(self, update_username: bool, new_entry: str, id_user: int) -> bool:
        """
        Met à jour le username ou le mot de passe d'un utilisateur.

        Paramètres :
        ------------
        update_username : bool
            True pour modifier le username, False pour le mot de passe
        new_entry : str
            Nouvelle valeur (username ou hashed_password)
        id_user : int

        Renvoie :
        ---------
        bool : True si la ligne a été modifiée
        """
        col = "username" if update_username else "hashed_password"
        with self.conn.cursor() as cur:
            cur.execute(
                f"UPDATE users SET {col} = %s WHERE id_user = %s RETURNING id_user",
                [new_entry, id_user],
            )
            return cur.fetchone() is not None

    def is_username_taken(self, username: str) -> bool:
        """
        Vérifie si un username est déjà utilisé.

        Renvoie :
        ---------
        bool : True si le nom est pris, False s'il est libre
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS count FROM users WHERE username = %s", [username]
            )
            row = cur.fetchone()
            return row["count"] > 0 if row else False
