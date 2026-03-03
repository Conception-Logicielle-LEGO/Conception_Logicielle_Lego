from typing import Annotated

import duckdb
from fastapi import Depends, HTTPException
import psycopg2
import psycopg2.extras

from app.database.connexion_duckdb import DB_PATH
from app.database.connexion_postgresql import PG_CONFIG


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
