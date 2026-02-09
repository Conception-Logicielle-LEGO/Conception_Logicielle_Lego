from pathlib import Path

import duckdb


"""
Module de connexion à la base de données DuckDB
"""

# Chemin vers la base de données (à vérifier avec changement pythonpath)
DB_PATH = Path(__file__).parent.resolve() / "duckdb" / "lego.duckdb"
DB_TEST_PATH = Path(__file__).parent.resolve() / "duckdb" / "lego_test.duckdb"


def get_connection(read_only=True, test=False):
    """
    Obtient une connexion à la base de données DuckDB

    parameters :
    ------------
    read_only
        (bool): Si True, ouvre en lecture seule (recommandé pour les requêtes)

    returns :
    ------------
    duckdb.DuckDBPyConnection
        Connexion à la base

    Exemple:
        >>> conn = get_connection()
        >>> result = conn.execute("SELECT COUNT(*) FROM sets").fetchone()
        >>> print(result[0])
        >>> conn.close()
    """
    path = DB_PATH if test is False else DB_TEST_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"Base de données introuvable: {DB_PATH}\n"
            f"Exécutez d'abord: python {DB_PATH.parent}/db_init.py"
        )

    return duckdb.connect(str(DB_PATH), read_only=read_only)


def db_connection(read_only=True, test=False):
    """
    Context manager pour une connexion à la base de données
    Ferme automatiquement la connexion

    parameters:
    ------------
    read_only
        (bool): Si True, ouvre en lecture seule

    returns:
    ------------
    duckdb.DuckDBPyConnection
        Connexion à la base

    Exemple:
        >>> with db_connection() as conn:
        ...     df = conn.execute("SELECT * FROM sets LIMIT 10").df()
        ...     print(df)
    """
    conn = get_connection(read_only=read_only, test=test)
    try:
        yield conn
    finally:
        conn.close()


def get_table_count(table_name, test):
    """
    Retourne le nombre de lignes dans une table

    parameters:
    ------------
    table_name
        (str): Nom de la table

    Returns:
    ------------
    int: Nombre de lignes

    Exemple:
        >>> count = get_table_count('sets')
        >>> print(f"Nombre de sets: {count:,}")
    """
    with db_connection(test=test) as conn:
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        return result[0]
