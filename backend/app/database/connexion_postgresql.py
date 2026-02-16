"""
Connexion à PostgreSQL (données utilisateurs - READ/WRITE)
"""

from contextlib import contextmanager
import os

from dotenv import load_dotenv
import psycopg2
import psycopg2.extras


load_dotenv()

# Configuration PostgreSQL
PG_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB", "lego_users"),
    "user": os.getenv("POSTGRES_USER", "lego_user"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
}


@contextmanager
def postgres_connection():
    """Connexion PostgreSQL avec gestion automatique"""
    conn = psycopg2.connect(**PG_CONFIG)
    try:
        yield conn
        conn.commit()  # Commit automatique si succès
    except Exception as e:
        conn.rollback()  # Rollback si erreur
        raise e
    finally:
        conn.close()


def execute_postgres_query(query, params=None, fetch=True):
    """Exécute une requête PostgreSQL"""
    with postgres_connection().cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    ) as cur:
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        return None


def execute_postgres_insert(query, params=None, returning=None):
    """Insert avec RETURNING"""
    with postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        if returning:
            return cur.fetchone()
        return None
