from fastapi import APIRouter, HTTPException

from app.api.dependencies import DuckDep, PgDep
from app.database.dao.user_parts_dao import UserPartsDAO
from app.dto.parts_dto import AddPartBody, UpdatePartQtyBody
from app.service.user_parts_service import UserPartsService


router = APIRouter(prefix="/users/{user_id}", tags=["parts"])


@router.get("/parts")
def get_owned_parts(user_id: int, pg: PgDep, duck: DuckDep):
    service = UserPartsService(UserPartsDAO(pg), pg)
    rows = service.get_owned_parts(user_id)
    if not rows:
        return []
    part_nums = list({r["part_num"] for r in rows})
    placeholders = ", ".join("?" * len(part_nums))
    detail_rows = duck.execute(
        f"""
        SELECT p.part_num, p.name,
               CASE WHEN e.element_id IS NOT NULL
                    THEN 'https://cdn.rebrickable.com/media/parts/elements/' || e.element_id || '.jpg'
                    ELSE 'https://cdn.rebrickable.com/media/parts/photos/' || p.part_num || '.jpg'
               END AS img_url
        FROM parts p
        LEFT JOIN (SELECT part_num, MIN(element_id) AS element_id FROM elements GROUP BY part_num) e
            ON p.part_num = e.part_num
        WHERE p.part_num IN ({placeholders})
        """,
        part_nums,
    ).fetchall()
    details = {r[0]: {"name": r[1], "img_url": r[2]} for r in detail_rows}
    return [
        {
            **row,
            **details.get(row["part_num"], {"name": row["part_num"], "img_url": None}),
        }
        for row in rows
    ]


@router.post("/parts", status_code=201)
def add_owned_part(user_id: int, body: AddPartBody, pg: PgDep):
    service = UserPartsService(UserPartsDAO(pg), pg)
    return service.add_part(
        user_id, body.part_num, body.color_id, body.quantity, is_used=body.is_used
    )


@router.delete("/parts/{part_num}/{color_id}", status_code=204)
def remove_owned_part(user_id: int, part_num: str, color_id: int, pg: PgDep):
    service = UserPartsService(UserPartsDAO(pg), pg)
    removed = service.remove_part(user_id, part_num, color_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Pièce non trouvée")


@router.put("/parts/{part_num}/{color_id}")
def update_owned_part_quantity(
    user_id: int, part_num: str, color_id: int, body: UpdatePartQtyBody, pg: PgDep
):
    service = UserPartsService(UserPartsDAO(pg), pg)
    updated = service.update_quantity(
        user_id, part_num, color_id, body.quantity, body.is_used
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Pièce non trouvée")
    return {"quantity": body.quantity}
