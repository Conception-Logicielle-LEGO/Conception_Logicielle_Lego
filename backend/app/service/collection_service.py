"""Service de gestion de la collection de sets d'un utilisateur."""

from app.database.dao.collection_dao import CollectionDAO


class CollectionService:
    """Service pour gérer la collection de sets d'un utilisateur.

    Gère les transactions (commit) après chaque opération d'écriture.
    """

    def __init__(self, dao: CollectionDAO, pg_conn):
        self.dao = dao
        self.conn = pg_conn

    def get_collection(self, user_id: int):
        return self.dao.get_user_collection(user_id)

    def add_set(self, user_id: int, set_num: str, is_built: bool = False):
        result = self.dao.add_set_to_collection(user_id, set_num, is_built)
        if result:
            self.conn.commit()
        return result  # None si doublon

    def remove_set(self, user_id: int, set_num: str) -> bool:
        removed = self.dao.remove_set_from_collection(user_id, set_num)
        self.conn.commit()
        return removed

    def mark_built(self, user_id: int, set_num: str, is_built: bool) -> bool:
        if is_built:
            updated = self.dao.mark_set_as_built(user_id, set_num)
        else:
            updated = self.dao.mark_set_as_unbuilt(user_id, set_num)
        if updated:
            self.conn.commit()
        return updated
