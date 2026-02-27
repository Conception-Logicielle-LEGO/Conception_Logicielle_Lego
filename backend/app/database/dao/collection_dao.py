"""Gère user_owned_sets"""

from datetime import datetime

from app.business_object.user_owned_set import UserOwnedSet


class CollectionDAO:
    """DAO pour gérer la collection de sets d'un utilisateur.

    IMPORTANT : ce DAO ne fait jamais de commit() explicite.
    La gestion des transactions (commit/rollback) est déléguée
    à l'appelant (service, test, context manager).
    Cela permet aux tests d'utiliser le rollback pour l'isolation.
    """

    def __init__(self, connection):
        self.connection = connection

    def add_set_to_collection(
        self, user_id: int, set_num: str, is_built: bool = False
    ) -> UserOwnedSet | None:
        """
        Ajoute un set à la collection d'un utilisateur.
        Utilise INSERT ... ON CONFLICT DO NOTHING pour éviter les doublons.
        Returns:
            Le UserOwnedSet ajouté, ou None si le set était déjà présent.
        """
        query = """
            INSERT INTO user_owned_sets (id_user, set_num, is_built, acquired_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id_user, set_num) DO NOTHING
            RETURNING id_user, set_num, is_built
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, set_num, is_built, datetime.now()))
            result = cur.fetchone()
            return UserOwnedSet.from_dict(dict(result)) if result else None

    def mark_set_as_built(self, user_id: int, set_num: str) -> bool:
        """
        Marque un set comme construit.
        Returns:
            True si mis à jour, False si le set n'existe pas.
        """
        query = """
            UPDATE user_owned_sets
            SET is_built = TRUE
            WHERE id_user = %s AND set_num = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, set_num))
            return cur.rowcount > 0

    def get_user_collection(self, user_id: int) -> list[UserOwnedSet]:
        """
        Récupère tous les sets de la collection d'un utilisateur.
        Returns:
            Liste de UserOwnedSet triés du plus récent au plus ancien.
        """
        query = """
            SELECT id_user, set_num, is_built
            FROM user_owned_sets
            WHERE id_user = %s
            ORDER BY acquired_date DESC
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            # RealDictCursor retourne des RealDictRow — convertir directement en dict
            return [UserOwnedSet.from_dict(dict(row)) for row in rows]

    def remove_set_from_collection(self, user_id: int, set_num: str) -> bool:
        """
        Retire un set de la collection.
        Returns:
            True si supprimé, False si le set n'était pas présent.
        """
        query = """
            DELETE FROM user_owned_sets
            WHERE id_user = %s AND set_num = %s
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (user_id, set_num))
            return cur.rowcount > 0
