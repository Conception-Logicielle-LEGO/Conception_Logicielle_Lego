"""Gère user_parts (pièces possédées/souhaitées)"""


class UserPartsDAO:
    """DAO pour gérer les pièces possédées ou souhaitées par un utilisateur.

    IMPORTANT : ce DAO ne fait jamais de commit() explicite.
    La gestion des transactions (commit/rollback) est déléguée à l'appelant.
    """

    def __init__(self, connection):
        self.connection = connection

    def add_part(
        self,
        user_id: int,
        part_num: str,
        color_id: int,
        status: str,
        quantity: int,
        is_used: bool = False,
    ):
        """Ajoute ou incrémente une pièce dans user_parts.

        En cas de conflit (même user/part/color), additionne les quantités
        et met à jour is_used.
        """
        query = """
            INSERT INTO user_parts (id_user, part_num, color_id, status, quantity, is_used)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_user, part_num, color_id, is_used)
            DO UPDATE SET
                quantity = user_parts.quantity + EXCLUDED.quantity
            RETURNING id_user, part_num, color_id, status, quantity, is_used
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, part_num, color_id, status, quantity, is_used))
            result = cur.fetchone()
            return dict(result) if result else None

    def remove_part(self, user_id: int, part_num: str, color_id: int) -> bool:
        """Supprime une pièce de user_parts.

        Returns:
            True si supprimé, False si inexistant.
        """
        query = """
            DELETE FROM user_parts
            WHERE id_user = %s AND part_num = %s AND color_id = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, part_num, color_id))
            return cur.rowcount > 0

    def get_owned_parts(self, user_id: int) -> list[dict]:
        """Récupère toutes les pièces possédées (status='owned')."""
        query = """
            SELECT id_user, part_num, color_id, quantity, status, is_used
            FROM user_parts
            WHERE id_user = %s AND status = 'owned'
            ORDER BY part_num, color_id, is_used
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            return [dict(row) for row in rows]

    def get_wished_parts(self, user_id: int) -> list[dict]:
        """Récupère toutes les pièces souhaitées (status='wished')."""
        query = """
            SELECT id_user, part_num, color_id, quantity, status
            FROM user_parts
            WHERE id_user = %s AND status = 'wished'
            ORDER BY part_num, color_id
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            return [dict(row) for row in rows]

    def update_quantity(
        self, user_id: int, part_num: str, color_id: int, quantity: int
    ) -> bool:
        """Met à jour la quantité d'une pièce.

        Returns:
            True si mis à jour, False si la pièce n'existe pas.
        """
        query = """
            UPDATE user_parts
            SET quantity = %s
            WHERE id_user = %s AND part_num = %s AND color_id = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (quantity, user_id, part_num, color_id))
            return cur.rowcount > 0
