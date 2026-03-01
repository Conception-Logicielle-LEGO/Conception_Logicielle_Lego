"""Service de gestion des sets favoris d'un utilisateur."""

from app.database.dao.favorite_dao import FavoriteDAO


class FavoriteService:
    """Service pour gérer les sets favoris d'un utilisateur.

    Gère les transactions (commit) après chaque opération d'écriture.
    """

    def __init__(self, dao: FavoriteDAO, pg_conn):
        self.dao = dao
        self.conn = pg_conn

    def get_favorites(self, user_id: int):
        return self.dao.get_user_favorites(user_id)

    def add_favorite(self, user_id: int, set_num: str):
        result = self.dao.add_favorite(user_id, set_num)
        if result:
            self.conn.commit()
        return result  # None si doublon

    def remove_favorite(self, user_id: int, set_num: str) -> bool:
        removed = self.dao.remove_favorite(user_id, set_num)
        self.conn.commit()
        return removed
