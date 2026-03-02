from fastapi import APIRouter

from app.api.dependencies import DuckDep, PgDep
from app.service.buildable_service import BuildableService


router = APIRouter(prefix="/users/{user_id}", tags=["buildable"])


@router.get("/buildable")
def get_buildable_sets(user_id: int, pg: PgDep, duck: DuckDep, limit: int = 50):
    service = BuildableService(pg, duck)
    result = service.get_buildable_sets(user_id, limit)
    return {key: [s.to_dict() for s in sets] for key, sets in result.items()}
