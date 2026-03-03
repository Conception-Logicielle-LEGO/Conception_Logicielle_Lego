"""Tests pour les utilitaires de connexion PostgreSQL.

Utilise des mocks pour éviter d'ouvrir de vraies connexions :
on teste le comportement (commit/rollback, retour des résultats),
pas l'infrastructure réseau.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.database.connexion_postgresql import (
    execute_postgres_insert,
    execute_postgres_query,
    postgres_connection,
)


MODULE = "app.database.connexion_postgresql"


class TestPostgresConnection:
    def test_context_manager_yields_connection(self):
        mock_conn = MagicMock()
        with (
            patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn),
            postgres_connection(test=True) as conn,
        ):
            assert conn is mock_conn

    def test_context_manager_commits_on_success(self):
        mock_conn = MagicMock()
        with (
            patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn),
            postgres_connection(test=True),
        ):
            pass
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_context_manager_rollbacks_on_exception(self):
        mock_conn = MagicMock()
        with (
            patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn),
            pytest.raises(ValueError),
            postgres_connection(test=True),
        ):
            raise ValueError("forced error")
        mock_conn.rollback.assert_called_once()
        mock_conn.commit.assert_not_called()


class TestExecutePostgresQuery:
    def test_select_returns_results(self):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value
        mock_cur.fetchall.return_value = [{"val": 1}]

        with patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn):
            result = execute_postgres_query("SELECT 1 AS val", test=True)
        assert result == [{"val": 1}]

    def test_select_with_params(self):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value
        mock_cur.fetchall.return_value = [{"val": 42}]

        with patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn):
            result = execute_postgres_query(
                "SELECT %s::int AS val", params=[42], test=True
            )
        assert result == [{"val": 42}]

    def test_no_fetch_returns_none(self):
        mock_conn = MagicMock()
        with patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn):
            result = execute_postgres_query("SELECT 1", fetch=False, test=True)
        assert result is None


class TestExecutePostgresInsert:
    def test_insert_without_returning(self):
        mock_conn = MagicMock()
        with patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn):
            result = execute_postgres_insert(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                ("conn_insert_user", "hash"),
                returning=False,
                test=True,
            )
        assert result is None

    def test_insert_with_returning(self):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value
        mock_cur.fetchone.return_value = (1,)

        with patch(f"{MODULE}.psycopg2.connect", return_value=mock_conn):
            result = execute_postgres_insert(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id_user",
                ("conn_returning_user", "hash"),
                returning=True,
                test=True,
            )
        assert result is not None
