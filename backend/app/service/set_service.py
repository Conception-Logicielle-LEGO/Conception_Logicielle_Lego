from business_object.user_owned_set import UserSetWithDetails
from database.dao.set_dao import SetDAO
from database.dao.user_dao import UserDAO


class SetService:
    """
    Service de gestion de la collection de sets d'un utilisateur.

    Responsabilités:
    - Gestion des sets possédés (ajout, suppression, marquage construit)
    - Récupération des informations de sets
    - Gestion automatique des pièces lors de l'ajout d'un set
    """

    def __init__(self, set_dao: SetDAO, user_dao: UserDAO):
        """
        Initialise le service avec les DAO nécessaires.

        Args:
            set_dao: DAO pour accéder aux sets
            user_dao: DAO pour accéder aux utilisateurs
        """
        self.set_dao = set_dao
        self.user_dao = user_dao

    def add_owned_set(self, id_user: int, set_num: str, is_built: bool = False) -> bool:
        """
        Ajoute un set à la collection de l'utilisateur.

        Vérifie que l'utilisateur et le set existent avant l'insertion.
        Si is_built=False, le set est ajouté comme "non construit".

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set (ex: "75192-1")
            is_built: Le set est-il déjà construit ? (défaut: False)

        Returns:
            bool: True si ajouté avec succès, False sinon

        Raises:
            ValueError: Si l'utilisateur n'existe pas
            ValueError: Si le set n'existe pas dans le catalogue
            ValueError: Si l'utilisateur possède déjà ce set
        """
        # 1. Vérifier que l'utilisateur existe
        if not self.user_dao.exists("id_user", id_user):
            raise ValueError(f"Utilisateur {id_user} introuvable")

        # 2. Vérifier que le set existe dans le catalogue Rebrickable
        if not self.set_dao.set_exists_in_catalog(set_num):
            raise ValueError(f"Set {set_num} introuvable dans le catalogue")

        # 3. Vérifier que l'utilisateur ne possède pas déjà ce set
        if self.set_dao.user_owns_set(id_user, set_num):
            raise ValueError(f"L'utilisateur {id_user} possède déjà le set {set_num}")

        # 4. Insérer dans user_owned_sets
        success = self.set_dao.add_owned_set(id_user, set_num, is_built)

        # 5. Si succès, ajouter les pièces du set aux pièces possédées
        if success:
            # TODO: Implémenter add_set_parts_to_user() plus tard
            # self.add_set_parts_to_user(id_user, set_num)
            pass

        return success

    def mark_as_built(self, id_user: int, set_num: str) -> bool:
        """
        Marque un set comme construit.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set

        Returns:
            bool: True si mis à jour avec succès, False sinon

        Raises:
            ValueError: Si l'utilisateur ne possède pas ce set
        """
        # Vérifier que l'utilisateur possède bien ce set
        if not self.set_dao.user_owns_set(id_user, set_num):
            raise ValueError(f"L'utilisateur {id_user} ne possède pas le set {set_num}")

        # Mettre à jour le statut
        return self.set_dao.mark_as_built(id_user, set_num, is_built=True)

    def mark_as_unbuilt(self, id_user: int, set_num: str) -> bool:
        """
        Marque un set comme non construit.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set

        Returns:
            bool: True si mis à jour avec succès, False sinon

        Raises:
            ValueError: Si l'utilisateur ne possède pas ce set
        """
        # Vérifier que l'utilisateur possède bien ce set
        if not self.set_dao.user_owns_set(id_user, set_num):
            raise ValueError(f"L'utilisateur {id_user} ne possède pas le set {set_num}")

        # Mettre à jour le statut
        return self.set_dao.mark_as_built(id_user, set_num, is_built=False)

    def get_user_sets(self, id_user: int) -> list[UserSetWithDetails]:
        """
        Récupère tous les sets possédés par un utilisateur avec leurs détails.

        Retourne une liste enrichie avec les informations du catalogue
        (nom, année, nombre de pièces, etc.).

        Args:
            id_user: ID de l'utilisateur

        Returns:
            list[UserSetWithDetails]: Liste des sets avec détails complets

        Raises:
            ValueError: Si l'utilisateur n'existe pas
        """
        # Vérifier que l'utilisateur existe
        if not self.user_dao.exists("id_user", id_user):
            raise ValueError(f"Utilisateur {id_user} introuvable")

        # Récupérer les sets avec JOIN sur le catalogue
        return self.set_dao.get_user_sets_with_details(id_user)

    def get_user_built_sets(self, id_user: int) -> list[UserSetWithDetails]:
        """
        Récupère uniquement les sets construits d'un utilisateur.

        Args:
            id_user: ID de l'utilisateur

        Returns:
            list[UserSetWithDetails]: Liste des sets construits
        """
        all_sets = self.get_user_sets(id_user)
        return [s for s in all_sets if s.is_built]

    def get_user_unbuilt_sets(self, id_user: int) -> list[UserSetWithDetails]:
        """
        Récupère uniquement les sets non construits d'un utilisateur.

        Args:
            id_user: ID de l'utilisateur

        Returns:
            list[UserSetWithDetails]: Liste des sets non construits
        """
        all_sets = self.get_user_sets(id_user)
        return [s for s in all_sets if not s.is_built]

    def remove_owned_set(self, id_user: int, set_num: str) -> bool:
        """
        Retire un set de la collection.

        Note: Cette méthode ne retire PAS automatiquement les pièces
        du set des pièces possédées, car l'utilisateur pourrait
        avoir obtenu ces pièces d'un autre set ou séparément.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set

        Returns:
            bool: True si supprimé avec succès, False sinon

        Raises:
            ValueError: Si l'utilisateur ne possède pas ce set
        """
        # Vérifier que l'utilisateur possède bien ce set
        if not self.set_dao.user_owns_set(id_user, set_num):
            raise ValueError(f"L'utilisateur {id_user} ne possède pas le set {set_num}")

        # Supprimer de user_owned_sets
        success = self.set_dao.remove_owned_set(id_user, set_num)

        # TODO (optionnel): Retirer les pièces du set ?
        # Problème: L'utilisateur peut avoir ces pièces d'un autre set
        # Solution future: Système de comptage avec status (libre/utilisé)

        return success

    def get_set_parts(self, set_num: str) -> list[dict]:
        """
        Récupère toutes les pièces nécessaires pour construire un set.

        Retourne la liste complète des pièces avec leurs quantités,
        couleurs et informations détaillées.

        Args:
            set_num: Numéro du set

        Returns:
            list[dict]: Liste de dicts avec:
                - part_num: Numéro de la pièce
                - color_id: ID de la couleur
                - quantity: Quantité nécessaire
                - part_name: Nom de la pièce
                - color_name: Nom de la couleur

        Raises:
            ValueError: Si le set n'existe pas dans le catalogue
        """
        # Vérifier que le set existe
        if not self.set_dao.set_exists_in_catalog(set_num):
            raise ValueError(f"Set {set_num} introuvable dans le catalogue")

        # Récupérer les pièces via inventories -> inventory_parts
        return self.set_dao.get_set_parts(set_num)

    def add_set_parts_to_user(self, id_user: int, set_num: str) -> bool:
        """
        Ajoute automatiquement toutes les pièces d'un set aux pièces possédées.

        IMPORTANT: Cette méthode nécessite l'implémentation de PartDAO
        et la table user_parts. Pour l'instant, elle retourne True
        sans rien faire.

        TODO: Implémenter quand PartDAO sera prêt.

        Args:
            id_user: ID de l'utilisateur
            set_num: Numéro du set

        Returns:
            bool: True si succès, False sinon

        Raises:
            ValueError: Si le set n'existe pas
        """
        # Vérifier que le set existe
        if not self.set_dao.set_exists_in_catalog(set_num):
            raise ValueError(f"Set {set_num} introuvable")

        # Récupérer toutes les pièces du set
        parts = self.get_set_parts(set_num)

        # TODO: Pour chaque pièce, INSERT ou UPDATE dans user_parts
        # Pseudo-code:
        # for part in parts:
        #     part_dao.add_or_update_user_part(
        #         id_user=id_user,
        #         part_num=part["part_num"],
        #         color_id=part["color_id"],
        #         quantity=part["quantity"],
        #         status="owned",
        #         is_used=False
        #     )

        print(
            f"TODO: Ajouter {len(parts)} pièces du set {set_num} à l'utilisateur {id_user}"
        )
        return True

    def get_set_details(self, set_num: str) -> dict | None:
        """
        Récupère les détails d'un set depuis le catalogue Rebrickable.

        Utile pour afficher les informations d'un set avant de l'ajouter.

        Args:
            set_num: Numéro du set

        Returns:
            dict | None: Détails du set ou None si inexistant
        """
        return self.set_dao.get_set_details(set_num)

    def count_user_sets(self, id_user: int) -> dict[str, int]:
        """
        Compte le nombre de sets possédés par un utilisateur.

        Args:
            id_user: ID de l'utilisateur

        Returns:
            dict avec:
                - total: Nombre total de sets
                - built: Nombre de sets construits
                - unbuilt: Nombre de sets non construits

        Raises:
            ValueError: Si l'utilisateur n'existe pas
        """
        all_sets = self.get_user_sets(id_user)

        total = len(all_sets)
        built = sum(1 for s in all_sets if s.is_built)
        unbuilt = total - built

        return {
            "total": total,
            "built": built,
            "unbuilt": unbuilt,
        }
