from fastapi import APIRouter

from app.api.dependencies import DuckDep
from app.database.dao.search_dao import SearchDAO
from app.service.search_service import SearchService


router = APIRouter(tags=["search"])


@router.get("/sets/search")
def search_sets(
    duck: DuckDep,
    q: str = "",
    theme_id: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int = 20,
):
    service = SearchService(SearchDAO(duck))
    return service.search_sets(q, theme_id, year_from, year_to, limit)


@router.get("/parts/search")
def search_parts(
    duck: DuckDep,
    q: str = "",
    color_id: int | None = None,
    category_id: int | None = None,
    limit: int = 20,
):
    service = SearchService(SearchDAO(duck))
    return service.search_parts(q, color_id, category_id, limit)


@router.get("/sets/recent")
def get_recent_sets(duck: DuckDep, limit: int = 12):
    service = SearchService(SearchDAO(duck))
    return service.get_recent_sets(limit)


@router.get("/stats")
def get_stats(duck: DuckDep):
    service = SearchService(SearchDAO(duck))
    return service.get_stats()
