"""
Initialisation de la base PostgreSQL (schémas prod et test).

Utilise une seule connexion pour initialiser les deux schémas,
car l'environnement limite le nombre de connexions simultanées.
"""

from pathlib import Path

import psycopg2

from app.database.connexion_postgresql import PG_CONFIG, SCHEMA_PROD, SCHEMA_TEST


def _init_schema(cur, schema: str, schema_sql: str) -> None:
    """Initialise un schéma donné en réutilisant un curseur existant."""
    print(f"🐘 Initialisation de PostgreSQL (schéma : {schema})...")
    cur.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE")
    cur.execute(f"CREATE SCHEMA {schema}")
    cur.execute(f"SET search_path TO {schema}")
    cur.execute(schema_sql)
    print(f"✅ Base PostgreSQL initialisée (schéma : {schema})")


def init_postgres_db(test: bool = False) -> None:
    """Initialise le schéma prod, ou prod + test si test=True.

    Une seule connexion est ouverte pour les deux opérations.

    Args:
        test: Si True, initialise aussi le schéma 'test'.
    """
    schema_sql = (Path(__file__).parent / "schema_user.sql").read_text()

    conn = psycopg2.connect(**PG_CONFIG)
    try:
        with conn.cursor() as cur:
            _init_schema(cur, SCHEMA_PROD, schema_sql)
            if test:
                _init_schema(cur, SCHEMA_TEST, schema_sql)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_postgres_db(test=True)  # initialise public ET test en une seule connexion
