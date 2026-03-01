from pathlib import Path

import duckdb
import psycopg2
import psycopg2.extras
import pytest

from app.database.connexion_duckdb import DB_TEST_PATH
from app.database.connexion_postgresql import PG_CONFIG, SCHEMA_TEST
from app.database.dao.collection_dao import CollectionDAO
from app.database.dao.favorite_dao import FavoriteDAO
from app.database.dao.user_parts_dao import UserPartsDAO
from app.database.dao.whishlist_dao import WishlistDAO


# ---------------------------------------------------------------------------
# PostgreSQL — connexion unique partagée sur toute la session
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def pg_conn():
    """
    Ouvre UNE SEULE connexion PostgreSQL pour toute la session de tests.

    Au démarrage :
      - Recrée le schéma 'test' depuis zéro (DROP + CREATE) pour garantir
        la cohérence avec schema_user.sql

    En cours de session :
      - pg_rollback annule les données après chaque test
    """
    schema_path = (
        Path(__file__).parent.parent
        / "app"
        / "database"
        / "postgres"
        / "schema_user.sql"
    )

    conn = psycopg2.connect(
        **PG_CONFIG,
        options=f"-c search_path={SCHEMA_TEST}",
        cursor_factory=psycopg2.extras.RealDictCursor,
    )

    try:
        with conn.cursor() as cur:
            # Recréer le schéma depuis zéro pour garantir la cohérence avec schema_user.sql
            cur.execute(f"DROP SCHEMA IF EXISTS {SCHEMA_TEST} CASCADE")
            cur.execute(f"CREATE SCHEMA {SCHEMA_TEST}")
            cur.execute(f"SET search_path TO {SCHEMA_TEST}")
            cur.execute(schema_path.read_text())
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        raise

    yield conn

    conn.close()


@pytest.fixture(autouse=True)
def pg_rollback(pg_conn):
    """
    Rollback AVANT et APRÈS chaque test.

    - Avant : remet la connexion dans un état propre si le test précédent
      a laissé la transaction en état 'aborted' (ex: UniqueViolation).
    - Après : annule les données écrites pendant le test.
    """
    pg_conn.rollback()  # <-- nettoyage AVANT le test
    yield
    pg_conn.rollback()  # <-- nettoyage APRÈS le test


@pytest.fixture()
def existing_user(pg_conn):
    """
    Insère un utilisateur de test et retourne son id_user.
    Nettoyé automatiquement par pg_rollback.
    """
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (username, hashed_password, email)
            VALUES (%s, %s, %s)
            RETURNING id_user
            """,
            ("test_user", "hashed_pw_placeholder", "test@lego.com"),
        )
        return cur.fetchone()["id_user"]


@pytest.fixture()
def dao_collection(pg_conn):
    return CollectionDAO(pg_conn)


@pytest.fixture()
def dao_favorite(pg_conn):
    return FavoriteDAO(pg_conn)


@pytest.fixture()
def dao_user_parts(pg_conn):
    return UserPartsDAO(pg_conn)


@pytest.fixture()
def dao_wishlist(pg_conn):
    return WishlistDAO(pg_conn)


# ---------------------------------------------------------------------------
# DuckDB
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def duckdb_conn():
    """
    Connexion DuckDB en lecture seule sur la base de test (lego_test.duckdb).
    Connexion unique pour toute la session (DuckDB read-only = pas d'isolation nécessaire).
    """
    if not DB_TEST_PATH.exists():
        pytest.skip(f"Base DuckDB de test introuvable : {DB_TEST_PATH}")

    conn = duckdb.connect(str(DB_TEST_PATH), read_only=True)
    yield conn
    conn.close()
