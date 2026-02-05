from database.connexion import db_connection
from typing import Optional


class UserDAO:
    def create_user(username, password) -> Optional[int]:
        """
        Create a new user in the database.
        ------------
        parameters
        username
            string: The username of the new user. Must be unique.
        password
            string: The password for the new user.
        """
        with db_connection(read_only=False) as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO users (username, password) VALUES (?, ?)
                    RETURNING id_user
                """,
                    [username, password],
                )
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error creating user: {e}")
                return None

    def delete_user(id_user):
        """
        Delete a user from the database by their ID.

        parameters:
        ------------
        id_user
            int: The ID of the user to delete.
        Example:
            >>> delete_user(1)
            User with ID 1 deleted.
        """
        with db_connection(read_only=False) as conn:
            conn.execute("DELETE FROM users WHERE id_user = ?", [id_user])

    def get_user(username=None, id_user=None) -> Optional[tuple]:
        """
        Get a user by either username or id_user. At least one of the parameters
        must be provided.

        parameters:
        ------------

        username
            string: The username of the user to retrieve.
            Optional if id_user is provided.
        id_user
            int: The ID of the user to retrieve. Optional if username is provided.

        returns:
        ------------
        tuple: A tuple containing the user's information (id_user, username, password)
        or None if the user is not found.

        """
        if username is None and id_user is None:
            raise ValueError("Either username or id_user must be provided.")
        with db_connection() as conn:
            if username is not None:
                result = conn.execute(
                    """
                    SELECT * FROM users WHERE username = ?
                """,
                    [username],
                ).fetchone()
            else:
                result = conn.execute(
                    """
                    SELECT * FROM users WHERE id_user = ?
                """,
                    [id_user],
                ).fetchone()
            return result

    # TODO: à déplacer dans autres DAO ?

    def get_owned_sets(id_user):
        pass

    def get_wishlist(id_user):
        pass

    def add_owned_set(id_user, set_num):
        pass

    def add_wishlist(id_user, piece_num):
        pass
