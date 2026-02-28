"""Gère favorite_sets"""


class FavoriteDAO:
    """DAO pour gérer les sets favoris d'un utilisateur."""

    def __init__(self, connection):
        """
        Initialise le DAO avec une connexion à la base de données.

        Args:
            connection: Connexion DuckDB ou PostgreSQL
        """
        self.connection = connection

    def add_favorite(self, user_id: int, set_num: str):
        """
        Ajoute un set aux favoris d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur
            set_num: Numéro du set LEGO
        """
        pass

    def remove_favorite(self, user_id: int, set_num: str):
        """
        Retire un set des favoris d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur
            set_num: Numéro du set LEGO
        """
        pass

    def get_user_favorites(self, user_id: int):
        """
        Récupère tous les sets favoris d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Liste des sets favoris
        """
        pass
