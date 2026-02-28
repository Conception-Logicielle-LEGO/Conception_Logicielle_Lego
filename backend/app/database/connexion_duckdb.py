"""
Connexion à DuckDB (données Rebrickable - READ ONLY)
"""

from contextlib import contextmanager
from pathlib import Path

import duckdb


DB_PATH = Path(__file__).parent / "duckdb" / "lego.duckdb"


@contextmanager
def duckdb_connection():
    """Connexion DuckDB en lecture seule"""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Base DuckDB introuvable: {DB_PATH}")

    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        yield conn
    finally:
        conn.close()


def execute_duckdb_query(query, params=None):
    """Exécute une requête sur DuckDB"""
    with duckdb_connection() as conn:
        result = conn.execute(query, params) if params else conn.execute(query)
        return result.fetchall()


def execute_duckdb_query_df(query, params=None):
    """Exécute une requête DuckDB et retourne un DataFrame"""
    with duckdb_connection() as conn:
        result = conn.execute(query, params) if params else conn.execute(query)
        return result.df()
