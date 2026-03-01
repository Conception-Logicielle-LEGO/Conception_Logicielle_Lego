"""Gère wishlist, wishlist_sets, wishlist_parts"""


class WishlistDAO:
    """DAO pour gérer la wishlist d'un utilisateur.

    IMPORTANT : ce DAO ne fait jamais de commit() explicite.
    La gestion des transactions (commit/rollback) est déléguée à l'appelant.
    """

    def __init__(self, connection):
        self.connection = connection

    def get_or_create_wishlist(self, user_id: int) -> int:
        """Retourne l'id_wishlist existant ou en crée un nouveau."""
        with self.connection.cursor() as cur:
            cur.execute(
                "SELECT id_wishlist FROM wishlist WHERE id_user = %s",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                return row["id_wishlist"]
            cur.execute(
                "INSERT INTO wishlist (id_user) VALUES (%s) RETURNING id_wishlist",
                (user_id,),
            )
            return cur.fetchone()["id_wishlist"]

    # --- Sets ---

    def add_set(self, user_id: int, set_num: str, priority: int = 0):
        """Ajoute un set à la wishlist. Ignoré si déjà présent."""
        wishlist_id = self.get_or_create_wishlist(user_id)
        query = """
            INSERT INTO wishlist_sets (id_wishlist, set_num, priority)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING id_wishlist, set_num, priority
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (wishlist_id, set_num, priority))
            result = cur.fetchone()
            return dict(result) if result else None

    def remove_set(self, user_id: int, set_num: str) -> bool:
        """Retire un set de la wishlist."""
        query = """
            DELETE FROM wishlist_sets
            WHERE id_wishlist IN (
                SELECT id_wishlist FROM wishlist WHERE id_user = %s
            ) AND set_num = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, set_num))
            return cur.rowcount > 0

    def get_sets(self, user_id: int) -> list[dict]:
        """Récupère tous les sets de la wishlist."""
        query = """
            SELECT ws.set_num, ws.priority, ws.added_at
            FROM wishlist_sets ws
            JOIN wishlist w ON ws.id_wishlist = w.id_wishlist
            WHERE w.id_user = %s
            ORDER BY ws.priority DESC, ws.added_at DESC
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            return [dict(row) for row in rows]

    # --- Pièces ---

    def add_part(self, user_id: int, part_num: str, color_id: int, quantity: int = 1):
        """Ajoute ou met à jour une pièce dans la wishlist."""
        wishlist_id = self.get_or_create_wishlist(user_id)
        query = """
            INSERT INTO wishlist_parts (id_wishlist, part_num, color_id, quantity)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id_wishlist, part_num, color_id)
            DO UPDATE SET quantity = EXCLUDED.quantity
            RETURNING id_wishlist, part_num, color_id, quantity
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (wishlist_id, part_num, color_id, quantity))
            result = cur.fetchone()
            return dict(result) if result else None

    def remove_part(self, user_id: int, part_num: str, color_id: int) -> bool:
        """Retire une pièce de la wishlist."""
        query = """
            DELETE FROM wishlist_parts
            WHERE id_wishlist IN (
                SELECT id_wishlist FROM wishlist WHERE id_user = %s
            ) AND part_num = %s AND color_id = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, part_num, color_id))
            return cur.rowcount > 0

    def get_parts(self, user_id: int) -> list[dict]:
        """Récupère toutes les pièces de la wishlist."""
        query = """
            SELECT wp.part_num, wp.color_id, wp.quantity, wp.added_at
            FROM wishlist_parts wp
            JOIN wishlist w ON wp.id_wishlist = w.id_wishlist
            WHERE w.id_user = %s
            ORDER BY wp.added_at DESC
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            return [dict(row) for row in rows]
