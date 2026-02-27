"""
Connexion à DuckDB (données Rebrickable - READ ONLY)
"""

from contextlib import contextmanager
from pathlib import Path

import duckdb


DB_PATH = Path(__file__).parent / "duckdb" / "lego.duckdb"
DB_TEST_PATH = Path(__file__).parent / "duckdb" / "lego_test.duckdb"


@contextmanager
def duckdb_connection(test: bool = False):
    """Connexion DuckDB en lecture seule.

    Args:
        test: Si True, utilise la base de test (lego_test.duckdb).
    """
    path = DB_TEST_PATH if test else DB_PATH

    if not path.exists():
        raise FileNotFoundError(f"Base DuckDB introuvable : {path}")

    conn = duckdb.connect(str(path), read_only=True)
    try:
        yield conn
    finally:
        conn.close()


def execute_duckdb_query(query: str, params=None, test: bool = False):
    """Exécute une requête sur DuckDB et retourne les lignes.

    Args:
        query: Requête SQL.
        params: Paramètres de la requête (optionnel).
        test: Si True, utilise la base de test.
    """
    with duckdb_connection(test=test) as conn:
        result = conn.execute(query, params) if params else conn.execute(query)
        return result.fetchall()


def execute_duckdb_query_df(query: str, params=None, test: bool = False):
    """Exécute une requête DuckDB et retourne un DataFrame.

    Args:
        query: Requête SQL.
        params: Paramètres de la requête (optionnel).
        test: Si True, utilise la base de test.
    """
    with duckdb_connection(test=test) as conn:
        result = conn.execute(query, params) if params else conn.execute(query)
        return result.df()
