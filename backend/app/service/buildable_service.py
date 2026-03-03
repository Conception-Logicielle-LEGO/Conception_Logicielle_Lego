"""Algorithme de matching cross-DB pour trouver les sets constructibles."""

from app.business_object.buildable_set import BuildableSet
from app.database.dao.collection_dao import CollectionDAO
from app.database.dao.user_parts_dao import UserPartsDAO


# Colonnes SQL communes aux 3 requêtes, aliasées pour coller aux champs de BuildableSet
_SELECT_COLS = """
    c.set_num, s.name, s.year, s.theme_id, s.num_parts, s.img_url,
    c.covered                                          AS parts_owned,
    c.total                                            AS total_parts_needed,
    ROUND(100.0 * c.covered / c.total, 1)              AS completion_percentage,
    (c.total - c.covered)                              AS missing_parts_count
"""

_STRICT_CTE = """
    WITH req AS (
        SELECT i.set_num, ip.part_num, ip.color_id, SUM(ip.quantity) AS needed
        FROM inventories i
        JOIN inventory_parts ip ON i.id = ip.inventory_id
        WHERE ip.is_spare = false
        GROUP BY i.set_num, ip.part_num, ip.color_id
    ),
    coverage AS (
        SELECT r.set_num,
            COUNT(*) AS total,
            SUM(CASE WHEN COALESCE(up.qty, 0) >= r.needed THEN 1 ELSE 0 END) AS covered
        FROM req r
        LEFT JOIN _user_parts up
            ON r.part_num = up.part_num AND r.color_id = up.color_id
        GROUP BY r.set_num
    )
"""


class BuildableService:
    """Détermine quels sets un utilisateur peut construire avec ses pièces.

    Stratégie :
    1. Récupère les pièces possédées depuis PostgreSQL.
    2. Pour chaque set non-construit de la collection, ajoute ses pièces
       au stock (car l'utilisateur les possède via le set).
    3. Charge le stock dans une table temporaire DuckDB.
    4. Deux requêtes DuckDB :
       - buildable : 100 % des (part_num, color_id) couverts
       - partial   : 80–99 % des (part_num, color_id) couverts
    """

    def __init__(self, pg_conn, duckdb_conn):
        self.user_parts_dao = UserPartsDAO(pg_conn)
        self.collection_dao = CollectionDAO(pg_conn)
        self.duck = duckdb_conn

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------

    def get_buildable_sets(self, user_id: int, limit: int = 50) -> dict:
        """Retourne deux listes de BuildableSet.

        Returns:
            {
              "buildable": list[BuildableSet],  # 100 %, couleur exacte
              "partial":   list[BuildableSet],  # 80–99 %, couleur exacte
            }
        """
        self._load_user_stock(user_id)

        collection = self.collection_dao.get_user_collection(user_id)
        collection_nums = [s.set_num for s in collection]

        buildable = self._query_buildable(collection_nums, limit)
        partial = self._query_partial(collection_nums, limit)

        return {
            "buildable": buildable,
            "partial": partial,
        }

    # ------------------------------------------------------------------
    # Méthodes privées
    # ------------------------------------------------------------------

    def _load_user_stock(self, user_id: int) -> None:
        """Construit et charge la table temporaire _user_parts dans DuckDB."""
        # Pièces possédées en propre
        owned_rows = self.user_parts_dao.get_owned_parts(user_id)
        owned_parts: dict[tuple, int] = {
            (row["part_num"], row["color_id"]): row["quantity"] for row in owned_rows
        }

        # Pièces des sets non construits (l'utilisateur possède les pièces)
        collection = self.collection_dao.get_user_collection(user_id)
        unbuilt_nums = [s.set_num for s in collection if not s.is_built]
        if unbuilt_nums:
            placeholders = ", ".join(["?"] * len(unbuilt_nums))
            rows = self.duck.execute(
                f"""
                SELECT ip.part_num, ip.color_id, SUM(ip.quantity) AS qty
                FROM inventories i
                JOIN inventory_parts ip ON i.id = ip.inventory_id
                WHERE i.set_num IN ({placeholders}) AND ip.is_spare = false
                GROUP BY ip.part_num, ip.color_id
                """,
                unbuilt_nums,
            ).fetchall()
            col_names = [d[0] for d in self.duck.description]
            for row in rows:
                r = dict(zip(col_names, row, strict=False))
                key = (r["part_num"], r["color_id"])
                owned_parts[key] = owned_parts.get(key, 0) + r["qty"]

        # Charger dans la table temporaire
        self.duck.execute(
            "CREATE TEMP TABLE IF NOT EXISTS _user_parts "
            "(part_num VARCHAR, color_id INTEGER, qty INTEGER)"
        )
        self.duck.execute("DELETE FROM _user_parts")
        if owned_parts:
            self.duck.executemany(
                "INSERT INTO _user_parts VALUES (?, ?, ?)",
                [(k[0], k[1], v) for k, v in owned_parts.items()],
            )

    def _rows_to_buildable_sets(self, rows: list) -> list[BuildableSet]:
        col_names = [d[0] for d in self.duck.description]
        return [
            BuildableSet.from_dict(dict(zip(col_names, row, strict=False)))
            for row in rows
        ]

    def _make_exclude(self, nums: list[str]) -> tuple[str, list]:
        """Retourne (placeholder_sql, params) pour une clause NOT IN."""
        if not nums:
            return "NULL", []
        return ", ".join(["?"] * len(nums)), nums

    def _query_buildable(
        self, exclude_nums: list[str], limit: int
    ) -> list[BuildableSet]:
        ph, ex_params = self._make_exclude(exclude_nums)
        rows = self.duck.execute(
            f"""
            {_STRICT_CTE}
            SELECT {_SELECT_COLS}
            FROM coverage c
            JOIN sets s ON c.set_num = s.set_num
            WHERE c.covered = c.total
              AND c.total >= 5
              AND c.set_num NOT IN ({ph})
            ORDER BY s.num_parts DESC
            LIMIT ?
            """,
            ex_params + [limit],
        ).fetchall()
        return self._rows_to_buildable_sets(rows)

    def _query_partial(self, exclude_nums: list[str], limit: int) -> list[BuildableSet]:
        ph, ex_params = self._make_exclude(exclude_nums)
        rows = self.duck.execute(
            f"""
            {_STRICT_CTE}
            SELECT {_SELECT_COLS}
            FROM coverage c
            JOIN sets s ON c.set_num = s.set_num
            WHERE c.covered < c.total
              AND ROUND(100.0 * c.covered / c.total, 1) >= 80
              AND c.total >= 5
              AND c.set_num NOT IN ({ph})
            ORDER BY completion_percentage DESC, s.num_parts DESC
            LIMIT ?
            """,
            ex_params + [limit],
        ).fetchall()
        return self._rows_to_buildable_sets(rows)
