"""Gère user_parts (pièces possédées/souhaitées)"""


class UserPartsDAO:
    """DAO pour gérer les pièces possédées ou souhaitées par un utilisateur."""

    def __init__(self, connection):
        """
        Initialise le DAO avec une connexion à la base de données.

        Args:
            connection: Connexion DuckDB ou PostgreSQL
        """
        self.connection = connection

    def add_part(
        self, user_id: int, part_num: str, color_id: int, status: str, quantity: int
    ):
        """
        Ajoute une pièce à la collection ou wishlist d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur
            part_num: Numéro de référence de la pièce
            color_id: ID de la couleur
            status: Statut de la pièce ('owned' ou 'wished')
            quantity: Quantité de pièces
        """
        pass

    def get_owned_parts(self, user_id: int):
        """
        Récupère toutes les pièces possédées par un utilisateur.

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Liste des pièces avec leurs quantités
        """
        pass

    def get_wished_parts(self, user_id: int):
        """
        Récupère toutes les pièces souhaitées par un utilisateur.

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Liste des pièces souhaitées avec leurs quantités
        """
        pass
