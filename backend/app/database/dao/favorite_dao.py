"""Gère favorite_sets"""

from app.business_object.favorite_set import FavoriteSet


class FavoriteDAO:
    """DAO pour gérer les sets favoris d'un utilisateur."""

    def __init__(self, connection):
        """
        Initialise le DAO avec une connexion à la base de données.

        Args:
            connection: Connexion PostgreSQL
        """
        self.connection = connection

    def add_favorite(self, user_id: int, set_num: str) -> FavoriteSet | None:
        """
        Ajoute un set aux favoris d'un utilisateur.
        Utilise INSERT ... ON CONFLICT DO NOTHING pour éviter les doublons.
        Returns:
            Le FavoriteSet ajouté, ou None si déjà présent.
        """
        query = """
            INSERT INTO favorite_sets (id_user, set_num)
            VALUES (%s, %s)
            ON CONFLICT (id_user, set_num) DO NOTHING
            RETURNING id_user, set_num, added_at
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, set_num))
            result = cur.fetchone()
            return FavoriteSet.from_dict(dict(result)) if result else None

    def remove_favorite(self, user_id: int, set_num: str) -> bool:
        """
        Retire un set des favoris d'un utilisateur.
        Returns:
            True si supprimé, False si le set n'était pas dans les favoris.
        """
        query = """
            DELETE FROM favorite_sets
            WHERE id_user = %s AND set_num = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, set_num))
            return cur.rowcount > 0

    def get_user_favorites(self, user_id: int) -> list[FavoriteSet]:
        """
        Récupère tous les sets favoris d'un utilisateur.
        Returns:
            Liste de FavoriteSet triés du plus récent au plus ancien.
        """
        query = """
            SELECT id_user, set_num, added_at
            FROM favorite_sets
            WHERE id_user = %s
            ORDER BY added_at DESC
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            return [FavoriteSet.from_dict(dict(row)) for row in rows]
