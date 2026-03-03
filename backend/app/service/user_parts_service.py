"""Service de gestion des pièces possédées/souhaitées d'un utilisateur."""

from app.database.dao.user_parts_dao import UserPartsDAO


class UserPartsService:
    """Service pour gérer les pièces d'un utilisateur.

    Gère les transactions (commit) après chaque opération d'écriture.
    """

    def __init__(self, dao: UserPartsDAO, pg_conn):
        self.dao = dao
        self.conn = pg_conn

    def add_part(
        self,
        user_id: int,
        part_num: str,
        color_id: int,
        quantity: int,
        status: str = "owned",
        is_used: bool = False,
    ):
        result = self.dao.add_part(
            user_id, part_num, color_id, status, quantity, is_used
        )
        self.conn.commit()
        return result

    def remove_part(self, user_id: int, part_num: str, color_id: int) -> bool:
        result = self.dao.remove_part(user_id, part_num, color_id)
        self.conn.commit()
        return result

    def update_quantity(
        self,
        user_id: int,
        part_num: str,
        color_id: int,
        quantity: int,
        is_used: bool = False,
    ) -> bool:
        result = self.dao.update_quantity(
            user_id, part_num, color_id, quantity, is_used
        )
        self.conn.commit()
        return result

    def get_owned_parts(self, user_id: int) -> list[dict]:
        return self.dao.get_owned_parts(user_id)

    def get_wished_parts(self, user_id: int) -> list[dict]:
        return self.dao.get_wished_parts(user_id)
