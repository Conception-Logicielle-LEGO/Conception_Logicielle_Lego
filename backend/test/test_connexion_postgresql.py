"""Tests pour les utilitaires de connexion PostgreSQL."""

from app.database.connexion_postgresql import (
    postgres_connection,
    execute_postgres_query,
    execute_postgres_insert,
    SCHEMA_TEST,
)


class TestPostgresConnection:
    def test_context_manager_yields_connection(self):
        with postgres_connection(test=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS val")
                row = cur.fetchone()
        assert row[0] == 1

    def test_context_manager_commits_on_success(self):
        with postgres_connection(test=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                    ("conn_test_commit", "hash"),
                )

    def test_context_manager_rollbacks_on_exception(self):
        import pytest
        with pytest.raises(ValueError):
            with postgres_connection(test=True) as conn:
                raise ValueError("forced error")


class TestExecutePostgresQuery:
    def test_select_returns_results(self):
        result = execute_postgres_query("SELECT 1 AS val", test=True)
        assert result[0]["val"] == 1

    def test_select_with_params(self):
        result = execute_postgres_query(
            "SELECT %s::int AS val", params=[42], test=True
        )
        assert result[0]["val"] == 42

    def test_no_fetch_returns_none(self):
        result = execute_postgres_query("SELECT 1", fetch=False, test=True)
        assert result is None


class TestExecutePostgresInsert:
    def test_insert_without_returning(self):
        result = execute_postgres_insert(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
            ("conn_insert_user", "hash"),
            returning=False,
            test=True,
        )
        assert result is None

    def test_insert_with_returning(self):
        result = execute_postgres_insert(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id_user",
            ("conn_returning_user", "hash"),
            returning=True,
            test=True,
        )
        assert result is not None
