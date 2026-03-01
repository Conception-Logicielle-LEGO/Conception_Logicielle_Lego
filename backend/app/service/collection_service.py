# app/service/collection_service.py

from app.business_object.user_owned_set import UserSetWithDetails
from app.database.dao.collection_dao import CollectionDAO


class CollectionService:
    """Gère la collection de sets d'un utilisateur."""

    def __init__(self, collection_dao: CollectionDAO):
        self.collection_dao = collection_dao

    def add_set_to_collection(
        self, user_id: int, set_num: str, is_built: bool = False
    ) -> bool:
        """Ajoute un set à la collection."""
        pass

    def remove_set_from_collection(self, user_id: int, set_num: str) -> bool:
        """Retire un set de la collection."""
        pass

    def mark_as_built(self, user_id: int, set_num: str) -> bool:
        """Marque un set comme construit."""
        pass

    def get_user_collection(self, user_id: int) -> list[UserSetWithDetails]:
        """Récupère la collection avec détails (JOIN Python)."""
        pass

    def get_collection_stats(self, user_id: int) -> dict:
        """Statistiques : nb sets total, nb construits, nb pièces total."""
        pass
