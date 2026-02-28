"""
Initialisation de la base PostgreSQL
"""

from pathlib import Path

from backend.app.database.connexion_postgresql import PG_CONFIG
import psycopg2


def init_postgres_db():
    """Initialise la base PostgreSQL"""
    print("🐘 Initialisation de PostgreSQL...")

    # Connexion
    conn = psycopg2.connect(**PG_CONFIG)
    cur = conn.cursor()

    # Lire le schema
    schema_path = Path(__file__).parent / "schema_user.sql"
    with open(schema_path) as f:
        schema_sql = f.read()

    # Exécuter
    cur.execute(schema_sql)
    conn.commit()

    print("✅ Base PostgreSQL initialisée")

    cur.close()
    conn.close()


if __name__ == "__main__":
    init_postgres_db()
