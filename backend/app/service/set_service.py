from database.dao.set_dao import SetDAO
from database.dao.user_dao import UserDAO


class SetService:
    """Service de gestion de la collection de sets d'un utilisateur."""

    def __init__(self, set_dao: SetDAO, user_dao: UserDAO):
        """
        Initialise le service.

        Args:
            set_dao: DAO pour accéder aux sets
            user_dao: DAO pour accéder aux utilisateurs
        """
        self.set_dao = set_dao
        self.user_dao = user_dao

    def add_owned_set(self, id_user: int, set_num: str, is_built: bool = False) -> bool:
        """
        Ajoute un set à la collection de l'utilisateur.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set (ex: "75192-1")
            is_built: Le set est-il déjà construit ?

        Returns:
            True si ajouté avec succès, False sinon
        """
        # TODO: Vérifier que l'utilisateur existe
        # TODO: Vérifier que le set existe dans le catalogue
        # TODO: Insérer dans user_owned_sets
        # TODO: Si succès, ajouter les pièces du set aux pièces possédées
        raise NotImplementedError

    def mark_as_built(self, id_user: int, set_num: str) -> bool:
        """
        Marque un set comme construit.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set

        Returns:
            True si mis à jour avec succès, False sinon
        """
        # TODO: UPDATE user_owned_sets SET is_built = TRUE WHERE ...
        raise NotImplementedError

    def get_user_sets(self, id_user: int) -> list[dict]:
        """
        Récupère tous les sets possédés par un utilisateur.

        Args:
            id_user: ID de l'utilisateur

        Returns:
            Liste de dicts avec set_num, name, is_built, etc.
        """
        # TODO: JOIN user_owned_sets avec sets pour avoir les infos complètes
        raise NotImplementedError

    def remove_owned_set(self, id_user: int, set_num: str) -> bool:
        """
        Retire un set de la collection.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set

        Returns:
            True si supprimé avec succès, False sinon
        """
        # TODO: DELETE FROM user_owned_sets WHERE ...
        # TODO: Optionnel: retirer les pièces du set des pièces possédées
        raise NotImplementedError

    def get_set_parts(self, set_num: str) -> list[dict]:
        """
        Récupère toutes les pièces d'un set via son inventaire.

        Args:
            set_num: Numéro du set

        Returns:
            Liste de dicts avec part_num, color_id, quantity
        """
        # TODO: Query inventories -> inventory_parts pour ce set
        raise NotImplementedError

    def add_set_parts_to_user(self, id_user: int, set_num: str) -> bool:
        """
        Ajoute automatiquement toutes les pièces d'un set aux pièces possédées.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set

        Returns:
            True si succès, False sinon
        """
        # TODO: Récupérer les pièces du set
        # TODO: Pour chaque pièce, INSERT ou UPDATE dans user_parts
        raise NotImplementedError
