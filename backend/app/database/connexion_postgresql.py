"""
Connexion à PostgreSQL (données utilisateurs - READ/WRITE)
"""

from contextlib import contextmanager
import os

from dotenv import load_dotenv
import psycopg2
import psycopg2.extras


load_dotenv()

# Schémas
SCHEMA_PROD = "public"
SCHEMA_TEST = "test"

# Mot de passe obligatoire
_pg_password = os.getenv("POSTGRES_PASSWORD")
if not _pg_password:
    raise OSError(
        "La variable d'environnement POSTGRES_PASSWORD n'est pas définie."
    )  # pragma: no cover

# Configuration PostgreSQL (même serveur pour prod et test)
PG_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB", "lego_users"),
    "user": os.getenv("POSTGRES_USER", "lego_user"),
    "password": _pg_password,
}


@contextmanager
def postgres_connection(test: bool = False):
    """Connexion PostgreSQL avec gestion automatique commit/rollback.

    Args:
        test: Si True, utilise le schéma 'test' au lieu de 'public'.
              Toutes les requêtes de la session cibleront ce schéma.
    """
    schema = SCHEMA_TEST if test else SCHEMA_PROD
    conn = psycopg2.connect(**PG_CONFIG, options=f"-c search_path={schema}")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_postgres_query(
    query: str, params=None, fetch: bool = True, test: bool = False
):
    """Exécute une requête PostgreSQL.

    Args:
        query: Requête SQL.
        params: Paramètres de la requête (optionnel).
        fetch: Si True, retourne les résultats.
        test: Si True, utilise le schéma de test.
    """
    with (
        postgres_connection(test=test) as conn,
        conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur,
    ):
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
    return None


def execute_postgres_insert(
    query: str, params=None, returning: bool = False, test: bool = False
):
    """Insert avec RETURNING optionnel.

    Args:
        query: Requête SQL INSERT.
        params: Paramètres de la requête (optionnel).
        returning: Si True, retourne la ligne insérée.
        test: Si True, utilise le schéma de test.
    """
    with postgres_connection(test=test) as conn, conn.cursor() as cur:
        cur.execute(query, params)
        if returning:
            return cur.fetchone()
    return None
