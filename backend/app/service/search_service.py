"""Service de recherche dans le catalogue LEGO (DuckDB, read-only)."""

from app.database.dao.search_dao import SearchDAO


class SearchService:
    """Wrapper autour de SearchDAO — pas de commit (DuckDB read-only)."""

    def __init__(self, dao: SearchDAO):
        self.dao = dao

    def search_sets(
        self,
        query: str = "",
        theme_id: int | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        limit: int = 20,
    ) -> list[dict]:
        return self.dao.search_sets(query, theme_id, year_from, year_to, limit)

    def search_parts(
        self,
        query: str = "",
        color_id: int | None = None,
        category_id: int | None = None,
        limit: int = 20,
    ) -> list[dict]:
        return self.dao.search_parts(query, color_id, category_id, limit)

    def get_recent_sets(self, limit: int = 12) -> list[dict]:
        return self.dao.get_recent_sets(limit)

    def get_stats(self) -> dict:
        return self.dao.get_stats()
