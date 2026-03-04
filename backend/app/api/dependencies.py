import threading
import time
from typing import Annotated

import duckdb
from fastapi import Depends, HTTPException
import psycopg2
import psycopg2.extras

from app.database.connexion_duckdb import DB_PATH
from app.database.connexion_postgresql import PG_CONFIG


_pg_conn: psycopg2.extensions.connection | None = None
_pg_lock = threading.Lock()


def _ensure_pg_conn() -> psycopg2.extensions.connection:
    """Crée ou valide la connexion persistante (thread-safe, avec retries)."""
    global _pg_conn
    with _pg_lock:
        for attempt in range(20):
            try:
                if _pg_conn is None or _pg_conn.closed:
                    _pg_conn = psycopg2.connect(
                        **PG_CONFIG,
                        cursor_factory=psycopg2.extras.RealDictCursor,
                    )
                else:
                    with _pg_conn.cursor() as cur:
                        cur.execute("SELECT 1")
                return _pg_conn
            except Exception:
                _pg_conn = None
                if attempt < 19:
                    time.sleep(2)
        raise ConnectionError("PostgreSQL inaccessible après plusieurs tentatives")
    return _pg_conn


def get_pg():
    """Connexion PostgreSQL persistante — jamais fermée pour garder le port-forward kubectl ouvert."""
    try:
        yield _ensure_pg_conn()
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e


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
