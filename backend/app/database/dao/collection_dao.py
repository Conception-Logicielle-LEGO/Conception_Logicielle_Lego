"""Gère user_owned_sets"""


class CollectionDAO:
    """DAO pour gérer la collection de sets d'un utilisateur."""

    def __init__(self, connection):
        """
        Initialise le DAO avec une connexion à la base de données.

        Args:
            connection: Connexion DuckDB ou PostgreSQL
        """
        self.connection = connection

    def add_set_to_collection(self, user_id: int, set_num: str, is_built: bool = False):
        """
        Ajoute un set à la collection d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur
            set_num: Numéro du set LEGO
            is_built: Indique si le set est déjà construit (défaut: False)
        """
        pass

    def mark_set_as_built(self, user_id: int, set_num: str):
        """
        Marque un set comme construit dans la collection.

        Args:
            user_id: ID de l'utilisateur
            set_num: Numéro du set LEGO
        """
        pass

    def get_user_collection(self, user_id: int):
        """
        Récupère tous les sets de la collection d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Liste des sets avec leur statut (construit/non construit)
        """
        pass

    def remove_set_from_collection(self, user_id: int, set_num: str):
        """
        Retire un set de la collection d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur
            set_num: Numéro du set LEGO
        """
        pass
