from business_object.user import User


class UserDAO:
    def __init__(self, db_connection):
        self.conn = db_connection(read_only=False)

    def create_user(self, user: User) -> User | None:
        """
        Créer un nouvel utilisateur dans la base de données
        ------------
        Paramètres
        user : utilisateur de type User sans id_user

        Renvoie
        un objet de type user avec l'id_user crée par la bdd
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

    def delete_user(self, id_user):
        """
        Supprime un utilisateur à partir de son id_user

        Paramètre:
        ------------
        id_user
            int: id de l'utilisateur à supprimer
        """
        self.conn.execute("DELETE FROM users WHERE id_user = ?", [id_user])

    def get_user(self, username=None, id_user=None) -> User | None:
        """
        Récupère un utilisateur à partir de son username ou id_user. Au moins l'un des deux paramètres doit
        être renseigné

        Paramètres
        ------------

        username
            string: username de l'utilisateur à renvoyer
        id_user
            int: id de l'utilisateur à renvoyer.

        Renvoie:
        ------------
        un objet de type User avec les informations de l'utilisateur
        ou None si l'utilisateur n'est pas trouvé

        """
        if username is None and id_user is None:
            raise ValueError("Either username or id_user must be provided.")
        if username is not None:
            result = self.conn.execute(
                """
                SELECT * FROM users WHERE username = ?
                """,
                [username],
            ).fetchone()
        else:
            result = self.conn.execute(
                """
                SELECT * FROM users WHERE id_user = ?
                """,
                [id_user],
            ).fetchone()
        id_user = result["id_user"]
        username = result["username"]
        password = result["password"]
        return User(username=username, id_user=id_user, password=password)

    def update_user(self, update_username: bool, new_entry, id_user):
        """
        DAO pour changer soit le username soit le mot de passe d'un utilisateur connecté

        Paramètres :
        update_username : bool pour savoir si on update le username ou le mot de passe
        new_entry : nouvelle entrée (ie nouveau username ou mot de passe déjà hashé)
        id_user : int

        Return :
        True si succès, False si echec
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
            ).fetchone
        return result is not None

    def is_username_taken(self, username):
        """
        Vérifie si un username est déjà utilisé
        Utile pour assurer l'unicité des usernames lors de l'inscription ou modification de profil des utilisateurs

        Paramètre :
        username : nom d'utilisateur à tester

        Renvoie :
        False si le nom est libre, True s'il est occupé"""
        result = self.conn.execute(
            """SELECT * FROM users WHERE username = %s;""", [username]
        ).fetchone()
        return result is not None

    # TODO: à déplacer dans autres DAO ?

    def get_owned_sets(self, id_user):
        pass

    def get_wishlist(self, id_user):
        pass

    def add_owned_set(self, id_user, set_num):
        pass

    def add_wishlist(self, id_user, piece_num):
        pass
