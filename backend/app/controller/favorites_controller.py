from fastapi import APIRouter, HTTPException

from app.api.dependencies import DuckDep, PgDep
from app.database.dao.favorite_dao import FavoriteDAO
from app.dto import AddFavoriteBody
from app.service.favorite_service import FavoriteService


router = APIRouter(prefix="/users/{user_id}", tags=["favorites"])


@router.get("/favorites")
def get_favorites(user_id: int, pg: PgDep, duck: DuckDep):
    favorites = FavoriteService(FavoriteDAO(pg), pg).get_favorites(user_id)
    if not favorites:
        return []
    set_nums = [f.set_num for f in favorites]
    placeholders = ", ".join("?" * len(set_nums))
    rows = duck.execute(
        f"SELECT set_num, name, year, num_parts, img_url FROM sets WHERE set_num IN ({placeholders})",
        set_nums,
    ).fetchall()
    details = {
        r[0]: dict(
            zip(["set_num", "name", "year", "num_parts", "img_url"], r, strict=False)
        )
        for r in rows
    }
    return [
        {**details.get(f.set_num, {"set_num": f.set_num}), "added_at": str(f.added_at)}
        for f in favorites
    ]


@router.post("/favorites", status_code=201)
def add_favorite(user_id: int, body: AddFavoriteBody, pg: PgDep):
    result = FavoriteService(FavoriteDAO(pg), pg).add_favorite(user_id, body.set_num)
    if result is None:
        raise HTTPException(status_code=409, detail="Set déjà dans les favoris")
    return result.to_dict()


@router.delete("/favorites/{set_num}", status_code=204)
def remove_favorite(user_id: int, set_num: str, pg: PgDep):
    removed = FavoriteService(FavoriteDAO(pg), pg).remove_favorite(user_id, set_num)
    if not removed:
        raise HTTPException(status_code=404, detail="Set non trouvé dans les favoris")
