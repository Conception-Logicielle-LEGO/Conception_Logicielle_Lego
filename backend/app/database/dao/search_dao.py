"""Recherche de sets et pièces dans DuckDB (embeddings VSS ou LIKE fallback)."""

try:
    from fastembed import TextEmbedding

    _st_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
except ImportError:  # pragma: no cover
    _st_model = None  # pragma: no cover


def _has_embeddings(conn) -> bool:
    """Vérifie si les tables d'embeddings existent."""
    try:
        conn.execute("SELECT 1 FROM set_embeddings LIMIT 1")
        return True
    except Exception:
        return False


def _has_vss(conn) -> bool:
    """Vérifie si l'extension VSS est disponible et chargée."""
    try:
        conn.execute("LOAD vss")
        return True
    except Exception:
        return False


class SearchDAO:
    """DAO de recherche sur DuckDB.

    Utilise les embeddings HNSW si disponibles,
    sinon tombe sur un LIKE basique.
    """

    def __init__(self, duckdb_conn):
        self.conn = duckdb_conn
        self._embeddings_ready = _has_embeddings(self.conn)
        self._vss_ready = (
            _st_model is not None and self._embeddings_ready and _has_vss(self.conn)
        )

    def _encode(self, query: str):
        """Encode une requête texte en vecteur float[384]."""
        if _st_model is None:
            raise RuntimeError("fastembed n'est pas installé")
        return next(iter(_st_model.embed([query]))).tolist()

    def search_sets(
        self,
        query: str,
        theme_id: int | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Recherche des sets par texte."""
        if self._vss_ready and query:
            return self._search_sets_vss(query, theme_id, year_from, year_to, limit)
        return self._search_sets_like(query, theme_id, year_from, year_to, limit)

    def _search_sets_vss(self, query, theme_id, year_from, year_to, limit):
        embedding = self._encode(query)
        conditions = []
        params = []

        if theme_id is not None:
            conditions.append("s.theme_id = ?")
            params.append(theme_id)
        if year_from is not None:
            conditions.append("s.year >= ?")
            params.append(year_from)
        if year_to is not None:
            conditions.append("s.year <= ?")
            params.append(year_to)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params_final = [embedding] + params + [limit]

        rows = self.conn.execute(
            f"""
            SELECT s.set_num, s.name, s.year, s.theme_id, s.num_parts, s.img_url,
                   array_distance(se.embedding, ?::FLOAT[384]) AS distance
            FROM set_embeddings se
            JOIN sets s ON se.set_num = s.set_num
            {where}
            ORDER BY distance ASC
            LIMIT ?
            """,
            params_final,
        ).fetchall()

        col_names = [d[0] for d in self.conn.description]
        return [dict(zip(col_names, row, strict=False)) for row in rows]

    def _search_sets_like(self, query, theme_id, year_from, year_to, limit):
        conditions = []
        params = []

        if query:
            conditions.append("(LOWER(s.name) LIKE ? OR s.set_num LIKE ?)")
            like = f"%{query.lower()}%"
            params.extend([like, like])
        if theme_id is not None:
            conditions.append("s.theme_id = ?")
            params.append(theme_id)
        if year_from is not None:
            conditions.append("s.year >= ?")
            params.append(year_from)
        if year_to is not None:
            conditions.append("s.year <= ?")
            params.append(year_to)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(limit)

        rows = self.conn.execute(
            f"""
            SELECT s.set_num, s.name, s.year, s.theme_id, s.num_parts, s.img_url
            FROM sets s
            {where}
            ORDER BY s.year DESC
            LIMIT ?
            """,
            params,
        ).fetchall()

        col_names = [d[0] for d in self.conn.description]
        return [dict(zip(col_names, row, strict=False)) for row in rows]

    def search_parts(
        self,
        query: str,
        color_id: int | None = None,
        category_id: int | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Recherche des pièces par texte."""
        if self._vss_ready and query:
            return self._search_parts_vss(query, color_id, category_id, limit)
        return self._search_parts_like(query, color_id, category_id, limit)

    def _search_parts_vss(self, query, color_id, category_id, limit):
        embedding = self._encode(query)
        conditions = []
        params = []

        if color_id is not None:
            # parts n'a pas de color_id direct — on filtre via elements (part↔color)
            conditions.append(
                "p.part_num IN (SELECT part_num FROM elements WHERE color_id = ?)"
            )
            params.append(color_id)
        if category_id is not None:
            conditions.append("p.part_cat_id = ?")
            params.append(category_id)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params_final = [embedding] + params + [limit]

        rows = self.conn.execute(
            f"""
            SELECT p.part_num, p.name, p.part_cat_id,
                   array_distance(pe.embedding, ?::FLOAT[384]) AS distance,
                   CASE WHEN e.element_id IS NOT NULL
                        THEN 'https://cdn.rebrickable.com/media/parts/elements/' || e.element_id || '.jpg'
                        ELSE 'https://cdn.rebrickable.com/media/parts/photos/' || p.part_num || '.jpg'
                   END AS img_url
            FROM part_embeddings pe
            JOIN parts p ON pe.part_num = p.part_num
            LEFT JOIN (SELECT part_num, MIN(element_id) AS element_id FROM elements GROUP BY part_num) e
                ON p.part_num = e.part_num
            {where}
            ORDER BY distance ASC
            LIMIT ?
            """,
            params_final,
        ).fetchall()

        col_names = [d[0] for d in self.conn.description]
        return [dict(zip(col_names, row, strict=False)) for row in rows]

    def _search_parts_like(self, query, _color_id, category_id, limit):
        conditions = []
        params = []

        if query:
            conditions.append("(LOWER(p.name) LIKE ? OR p.part_num LIKE ?)")
            like = f"%{query.lower()}%"
            params.extend([like, like])
        if category_id is not None:
            conditions.append("p.part_cat_id = ?")
            params.append(category_id)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(limit)

        rows = self.conn.execute(
            f"""
            SELECT p.part_num, p.name, p.part_cat_id,
                   CASE WHEN e.element_id IS NOT NULL
                        THEN 'https://cdn.rebrickable.com/media/parts/elements/' || e.element_id || '.jpg'
                        ELSE 'https://cdn.rebrickable.com/media/parts/photos/' || p.part_num || '.jpg'
                   END AS img_url
            FROM parts p
            LEFT JOIN (SELECT part_num, MIN(element_id) AS element_id FROM elements GROUP BY part_num) e
                ON p.part_num = e.part_num
            {where}
            ORDER BY p.name ASC
            LIMIT ?
            """,
            params,
        ).fetchall()

        col_names = [d[0] for d in self.conn.description]
        return [dict(zip(col_names, row, strict=False)) for row in rows]

    def get_recent_sets(self, limit: int = 12) -> list[dict]:
        """Retourne les sets les plus récents du catalogue."""
        rows = self.conn.execute(
            """
            SELECT set_num, name, year, theme_id, num_parts, img_url
            FROM sets
            ORDER BY year DESC
            LIMIT ?
            """,
            [limit],
        ).fetchall()
        col_names = [d[0] for d in self.conn.description]
        return [dict(zip(col_names, row, strict=False)) for row in rows]

    def get_stats(self) -> dict:
        """Retourne les statistiques globales du catalogue."""
        sets_count = self.conn.execute("SELECT COUNT(*) FROM sets").fetchone()[0]
        parts_count = self.conn.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
        themes_count = self.conn.execute("SELECT COUNT(*) FROM themes").fetchone()[0]
        return {
            "totalSets": sets_count,
            "totalParts": parts_count,
            "totalThemes": themes_count,
        }
