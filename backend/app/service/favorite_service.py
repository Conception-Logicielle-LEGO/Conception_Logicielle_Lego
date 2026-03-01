# app/service/favorite_service.py

from app.business_object.favorite_set_with_details import FavoriteSetWithDetails
from app.database.dao.favorite_dao import FavoriteDAO


class FavoriteService:
    """Gère les sets favoris d'un utilisateur."""

    def __init__(self, favorite_dao: FavoriteDAO):
        self.favorite_dao = favorite_dao

    def add_to_favorites(self, user_id: int, set_num: str) -> bool:
        """Ajoute un set aux favoris."""
        pass

    def remove_from_favorites(self, user_id: int, set_num: str) -> bool:
        """Retire un set des favoris."""
        pass

    def get_user_favorites(self, user_id: int) -> list[FavoriteSetWithDetails]:
        """Récupère les favoris avec détails (JOIN Python)."""
        pass

    def is_favorite(self, user_id: int, set_num: str) -> bool:
        """Vérifie si un set est dans les favoris."""
        pass
