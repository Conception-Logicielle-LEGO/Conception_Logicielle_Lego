"""Service de gestion de la wishlist d'un utilisateur."""

from app.database.dao.whishlist_dao import WishlistDAO


class WishlistService:
    """Service pour gérer la wishlist d'un utilisateur.

    Gère les transactions (commit) après chaque opération d'écriture.
    """

    def __init__(self, dao: WishlistDAO, pg_conn):
        self.dao = dao
        self.conn = pg_conn

    # --- Sets ---

    def add_set(self, user_id: int, set_num: str, priority: int = 0):
        result = self.dao.add_set(user_id, set_num, priority)
        self.conn.commit()
        return result

    def remove_set(self, user_id: int, set_num: str) -> bool:
        result = self.dao.remove_set(user_id, set_num)
        self.conn.commit()
        return result

    def get_sets(self, user_id: int) -> list[dict]:
        return self.dao.get_sets(user_id)

    # --- Pièces ---

    def add_part(self, user_id: int, part_num: str, color_id: int, quantity: int = 1):
        result = self.dao.add_part(user_id, part_num, color_id, quantity)
        self.conn.commit()
        return result

    def remove_part(self, user_id: int, part_num: str, color_id: int) -> bool:
        result = self.dao.remove_part(user_id, part_num, color_id)
        self.conn.commit()
        return result

    def get_parts(self, user_id: int) -> list[dict]:
        return self.dao.get_parts(user_id)

    def update_part_quantity(
        self, user_id: int, part_num: str, color_id: int, quantity: int
    ) -> bool:
        result = self.dao.update_part_quantity(user_id, part_num, color_id, quantity)
        self.conn.commit()
        return result
