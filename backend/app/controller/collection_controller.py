from fastapi import APIRouter, HTTPException

from app.api.dependencies import DuckDep, PgDep
from app.database.dao.collection_dao import CollectionDAO
from app.dto import AddSetBody, UpdateBuiltBody
from app.service.collection_service import CollectionService


router = APIRouter(prefix="/users/{user_id}", tags=["collection"])


@router.get("/collection")
def get_collection(user_id: int, pg: PgDep, duck: DuckDep):
    sets = CollectionService(CollectionDAO(pg), pg).get_collection(user_id)
    if not sets:
        return []
    set_nums = [s.set_num for s in sets]
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
        {**details.get(s.set_num, {"set_num": s.set_num}), "is_built": s.is_built}
        for s in sets
    ]


@router.post("/collection", status_code=201)
def add_to_collection(user_id: int, body: AddSetBody, pg: PgDep):
    result = CollectionService(CollectionDAO(pg), pg).add_set(
        user_id, body.set_num, body.is_built
    )
    if result is None:
        raise HTTPException(status_code=409, detail="Set déjà dans la collection")
    return result.to_dict()


@router.delete("/collection/{set_num}", status_code=204)
def remove_from_collection(user_id: int, set_num: str, pg: PgDep):
    removed = CollectionService(CollectionDAO(pg), pg).remove_set(user_id, set_num)
    if not removed:
        raise HTTPException(status_code=404, detail="Set non trouvé dans la collection")


@router.put("/collection/{set_num}/built")
def update_built_status(user_id: int, set_num: str, body: UpdateBuiltBody, pg: PgDep):
    updated = CollectionService(CollectionDAO(pg), pg).mark_built(
        user_id, set_num, body.is_built
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Set non trouvé dans la collection")
    return {"is_built": body.is_built}
