from fastapi import APIRouter, HTTPException

from app.api.dependencies import DuckDep, PgDep
from app.database.dao.whishlist_dao import WishlistDAO
from app.dto import AddWishlistPartBody, AddWishlistSetBody, UpdateWishlistPartQtyBody
from app.service.wishlist_service import WishlistService


router = APIRouter(prefix="/users/{user_id}", tags=["wishlist"])


@router.get("/wishlist/sets")
def get_wishlist_sets(user_id: int, pg: PgDep, duck: DuckDep):
    items = WishlistService(WishlistDAO(pg), pg).get_sets(user_id)
    if not items:
        return []
    set_nums = [it["set_num"] for it in items]
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
        {
            **details.get(it["set_num"], {"set_num": it["set_num"]}),
            "priority": it.get("priority"),
        }
        for it in items
    ]


@router.post("/wishlist/sets", status_code=201)
def add_wishlist_set(user_id: int, body: AddWishlistSetBody, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    result = service.add_set(user_id, body.set_num, body.priority)
    if result is None:
        raise HTTPException(status_code=409, detail="Set déjà dans la wishlist")
    return result


@router.delete("/wishlist/sets/{set_num}", status_code=204)
def remove_wishlist_set(user_id: int, set_num: str, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    removed = service.remove_set(user_id, set_num)
    if not removed:
        raise HTTPException(status_code=404, detail="Set non trouvé dans la wishlist")


@router.get("/wishlist/parts")
def get_wishlist_parts(user_id: int, pg: PgDep, duck: DuckDep):
    service = WishlistService(WishlistDAO(pg), pg)
    rows = service.get_parts(user_id)
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


@router.post("/wishlist/parts", status_code=201)
def add_wishlist_part(user_id: int, body: AddWishlistPartBody, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    return service.add_part(user_id, body.part_num, body.color_id, body.quantity)


@router.delete("/wishlist/parts/{part_num}/{color_id}", status_code=204)
def remove_wishlist_part(user_id: int, part_num: str, color_id: int, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    removed = service.remove_part(user_id, part_num, color_id)
    if not removed:
        raise HTTPException(
            status_code=404, detail="Pièce non trouvée dans la wishlist"
        )


@router.put("/wishlist/parts/{part_num}/{color_id}")
def update_wishlist_part_quantity(
    user_id: int,
    part_num: str,
    color_id: int,
    body: UpdateWishlistPartQtyBody,
    pg: PgDep,
):
    service = WishlistService(WishlistDAO(pg), pg)
    updated = service.update_part_quantity(user_id, part_num, color_id, body.quantity)
    if not updated:
        raise HTTPException(
            status_code=404, detail="Pièce non trouvée dans la wishlist"
        )
    return {"quantity": body.quantity}
