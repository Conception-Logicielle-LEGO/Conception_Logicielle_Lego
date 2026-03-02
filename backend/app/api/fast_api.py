from typing import Annotated

import duckdb
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
from pydantic import BaseModel
import uvicorn

from app.database.connexion_duckdb import DB_PATH
from app.database.connexion_postgresql import PG_CONFIG
from app.database.dao.collection_dao import CollectionDAO
from app.database.dao.favorite_dao import FavoriteDAO
from app.database.dao.search_dao import SearchDAO
from app.database.dao.user_parts_dao import UserPartsDAO
from app.database.dao.whishlist_dao import WishlistDAO
from app.service.buildable_service import BuildableService
from app.service.collection_service import CollectionService
from app.service.favorite_service import FavoriteService
from app.service.search_service import SearchService
from app.service.user_parts_service import UserPartsService
from app.service.wishlist_service import WishlistService


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="LEGO Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Lien avec le main
# ---------------------------------------------------------------------------


def run_app():
    """
    Starts the FastAPI application using Uvicorn.
    - Runs on host 0.0.0.0 (accessible from outside container)
    - Port 8000
    - Reload enabled for development
    """
    uvicorn.run("backend.app.api.fast_api:app", host="0.0.0.0", port=8000, reload=True)


# ---------------------------------------------------------------------------
# Injection de dépendances
# ---------------------------------------------------------------------------


_pg_conn: psycopg2.extensions.connection | None = None


def get_pg():
    """Connexion PostgreSQL persistante — jamais fermée pour garder le port-forward kubectl ouvert."""
    global _pg_conn
    try:
        if _pg_conn is None or _pg_conn.closed:
            _pg_conn = psycopg2.connect(
                **PG_CONFIG,
                cursor_factory=psycopg2.extras.RealDictCursor,
            )
        else:
            _pg_conn.cursor().execute("SELECT 1")
    except Exception:
        _pg_conn = psycopg2.connect(
            **PG_CONFIG,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
    yield _pg_conn


def get_duck():
    """Connexion DuckDB read-only — fermée après la requête."""
    if not DB_PATH.exists():
        raise HTTPException(status_code=503, detail="Base DuckDB introuvable")
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        yield conn
    finally:
        conn.close()


PgDep = Annotated[psycopg2.extensions.connection, Depends(get_pg)]
DuckDep = Annotated[duckdb.DuckDBPyConnection, Depends(get_duck)]


# ---------------------------------------------------------------------------
# Schémas Pydantic (body des requêtes POST)
# ---------------------------------------------------------------------------


class AddSetBody(BaseModel):
    set_num: str
    is_built: bool = False


class UpdateBuiltBody(BaseModel):
    is_built: bool


class AddPartBody(BaseModel):
    part_num: str
    color_id: int = 0
    quantity: int = 1
    is_used: bool = False


class AddWishlistSetBody(BaseModel):
    set_num: str
    priority: int = 0


class AddWishlistPartBody(BaseModel):
    part_num: str
    color_id: int
    quantity: int = 1


class AddFavoriteBody(BaseModel):
    set_num: str


# ---------------------------------------------------------------------------
# Recherche (DuckDB)
# ---------------------------------------------------------------------------


@app.get("/sets/search")
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


@app.get("/parts/search")
def search_parts(
    duck: DuckDep,
    q: str = "",
    color_id: int | None = None,
    category_id: int | None = None,
    limit: int = 20,
):
    service = SearchService(SearchDAO(duck))
    return service.search_parts(q, color_id, category_id, limit)


# ---------------------------------------------------------------------------
# Sets récents + stats (DuckDB)
# ---------------------------------------------------------------------------


@app.get("/sets/recent")
def get_recent_sets(duck: DuckDep, limit: int = 12):
    service = SearchService(SearchDAO(duck))
    return service.get_recent_sets(limit)


@app.get("/stats")
def get_stats(duck: DuckDep):
    service = SearchService(SearchDAO(duck))
    return service.get_stats()


# ---------------------------------------------------------------------------
# Collection utilisateur (PostgreSQL)
# ---------------------------------------------------------------------------


@app.get("/users/{user_id}/collection")
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


@app.post("/users/{user_id}/collection", status_code=201)
def add_to_collection(user_id: int, body: AddSetBody, pg: PgDep):
    result = CollectionService(CollectionDAO(pg), pg).add_set(
        user_id, body.set_num, body.is_built
    )
    if result is None:
        raise HTTPException(status_code=409, detail="Set déjà dans la collection")
    return result.to_dict()


@app.delete("/users/{user_id}/collection/{set_num}", status_code=204)
def remove_from_collection(user_id: int, set_num: str, pg: PgDep):
    removed = CollectionService(CollectionDAO(pg), pg).remove_set(user_id, set_num)
    if not removed:
        raise HTTPException(status_code=404, detail="Set non trouvé dans la collection")


@app.put("/users/{user_id}/collection/{set_num}/built")
def update_built_status(user_id: int, set_num: str, body: UpdateBuiltBody, pg: PgDep):
    updated = CollectionService(CollectionDAO(pg), pg).mark_built(
        user_id, set_num, body.is_built
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Set non trouvé dans la collection")
    return {"is_built": body.is_built}


# ---------------------------------------------------------------------------
# Pièces possédées (PostgreSQL)
# ---------------------------------------------------------------------------


@app.get("/users/{user_id}/parts")
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


@app.post("/users/{user_id}/parts", status_code=201)
def add_owned_part(user_id: int, body: AddPartBody, pg: PgDep):
    service = UserPartsService(UserPartsDAO(pg), pg)
    return service.add_part(
        user_id, body.part_num, body.color_id, body.quantity, is_used=body.is_used
    )


@app.delete("/users/{user_id}/parts/{part_num}/{color_id}", status_code=204)
def remove_owned_part(user_id: int, part_num: str, color_id: int, pg: PgDep):
    service = UserPartsService(UserPartsDAO(pg), pg)
    removed = service.remove_part(user_id, part_num, color_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Pièce non trouvée")


# ---------------------------------------------------------------------------
# Wishlist sets (PostgreSQL)
# ---------------------------------------------------------------------------


@app.get("/users/{user_id}/wishlist/sets")
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


@app.post("/users/{user_id}/wishlist/sets", status_code=201)
def add_wishlist_set(user_id: int, body: AddWishlistSetBody, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    result = service.add_set(user_id, body.set_num, body.priority)
    if result is None:
        raise HTTPException(status_code=409, detail="Set déjà dans la wishlist")
    return result


@app.delete("/users/{user_id}/wishlist/sets/{set_num}", status_code=204)
def remove_wishlist_set(user_id: int, set_num: str, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    removed = service.remove_set(user_id, set_num)
    if not removed:
        raise HTTPException(status_code=404, detail="Set non trouvé dans la wishlist")


# ---------------------------------------------------------------------------
# Wishlist pièces (PostgreSQL)
# ---------------------------------------------------------------------------


@app.get("/users/{user_id}/wishlist/parts")
def get_wishlist_parts(user_id: int, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    return service.get_parts(user_id)


@app.post("/users/{user_id}/wishlist/parts", status_code=201)
def add_wishlist_part(user_id: int, body: AddWishlistPartBody, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    return service.add_part(user_id, body.part_num, body.color_id, body.quantity)


@app.delete("/users/{user_id}/wishlist/parts/{part_num}/{color_id}", status_code=204)
def remove_wishlist_part(user_id: int, part_num: str, color_id: int, pg: PgDep):
    service = WishlistService(WishlistDAO(pg), pg)
    removed = service.remove_part(user_id, part_num, color_id)
    if not removed:
        raise HTTPException(
            status_code=404, detail="Pièce non trouvée dans la wishlist"
        )


# ---------------------------------------------------------------------------
# Favoris (PostgreSQL)
# ---------------------------------------------------------------------------


@app.get("/users/{user_id}/favorites")
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


@app.post("/users/{user_id}/favorites", status_code=201)
def add_favorite(user_id: int, body: AddFavoriteBody, pg: PgDep):
    result = FavoriteService(FavoriteDAO(pg), pg).add_favorite(user_id, body.set_num)
    if result is None:
        raise HTTPException(status_code=409, detail="Set déjà dans les favoris")
    return result.to_dict()


@app.delete("/users/{user_id}/favorites/{set_num}", status_code=204)
def remove_favorite(user_id: int, set_num: str, pg: PgDep):
    removed = FavoriteService(FavoriteDAO(pg), pg).remove_favorite(user_id, set_num)
    if not removed:
        raise HTTPException(status_code=404, detail="Set non trouvé dans les favoris")


# ---------------------------------------------------------------------------
# Sets constructibles (cross-DB)
# ---------------------------------------------------------------------------


@app.get("/users/{user_id}/buildable")
def get_buildable_sets(user_id: int, pg: PgDep, duck: DuckDep, limit: int = 50):
    service = BuildableService(pg, duck)
    result = service.get_buildable_sets(user_id, limit)
    return {key: [s.to_dict() for s in sets] for key, sets in result.items()}


# ---------------------------------------------------------------------------
# Endpoint de santé
# ---------------------------------------------------------------------------


@app.get("/health")
def health():
    return {"status": "ok"}
