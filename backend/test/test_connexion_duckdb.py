"""Tests pour les utilitaires de connexion DuckDB."""

import duckdb
import pytest
from unittest.mock import patch

from app.database.connexion_duckdb import (
    duckdb_connection,
    execute_duckdb_query,
    execute_duckdb_query_df,
)


@pytest.fixture
def temp_db(tmp_path):
    """Base DuckDB temporaire avec une table simple."""
    db_path = tmp_path / "test.duckdb"
    conn = duckdb.connect(str(db_path))
    conn.execute("CREATE TABLE items (id INTEGER, name VARCHAR)")
    conn.execute("INSERT INTO items VALUES (1, 'brick'), (2, 'plate')")
    conn.close()
    return db_path


class TestDuckdbConnection:
    def test_raises_file_not_found_when_db_missing(self, tmp_path):
        missing = tmp_path / "missing.duckdb"
        with patch("app.database.connexion_duckdb.DB_PATH", missing):
            with pytest.raises(FileNotFoundError):
                with duckdb_connection():
                    pass

    def test_yields_connection_when_db_exists(self, temp_db):
        with patch("app.database.connexion_duckdb.DB_PATH", temp_db):
            with duckdb_connection() as conn:
                result = conn.execute("SELECT COUNT(*) FROM items").fetchone()
                assert result[0] == 2

    def test_connection_yields_working_connection(self, temp_db):
        with patch("app.database.connexion_duckdb.DB_PATH", temp_db):
            with duckdb_connection() as conn:
                result = conn.execute("SELECT 1").fetchone()
                assert result[0] == 1


class TestExecuteDuckdbQuery:
    def test_query_without_params(self, temp_db):
        with patch("app.database.connexion_duckdb.DB_PATH", temp_db):
            result = execute_duckdb_query("SELECT name FROM items ORDER BY id")
        assert result[0][0] == "brick"

    def test_query_with_params(self, temp_db):
        with patch("app.database.connexion_duckdb.DB_PATH", temp_db):
            result = execute_duckdb_query("SELECT name FROM items WHERE id = ?", [2])
        assert result[0][0] == "plate"


class TestExecuteDuckdbQueryDf:
    def test_returns_dataframe(self, temp_db):
        with patch("app.database.connexion_duckdb.DB_PATH", temp_db):
            df = execute_duckdb_query_df("SELECT * FROM items ORDER BY id")
        assert len(df) == 2
        assert df["name"][0] == "brick"

    def test_dataframe_with_params(self, temp_db):
        with patch("app.database.connexion_duckdb.DB_PATH", temp_db):
            df = execute_duckdb_query_df("SELECT * FROM items WHERE id = ?", [1])
        assert len(df) == 1
        assert df["name"][0] == "brick"
