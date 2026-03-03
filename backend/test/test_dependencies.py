"""Tests pour les dépendances FastAPI (get_pg, get_duck)."""

from unittest.mock import MagicMock, patch

import duckdb
from fastapi import HTTPException
import pytest

import app.api.dependencies as dep_module
from app.api.dependencies import get_duck, get_pg


class TestGetPg:
    def test_creates_new_connection_when_none(self, monkeypatch):
        monkeypatch.setattr(dep_module, "_pg_conn", None)
        mock_conn = MagicMock()
        mock_conn.closed = False

        with patch("app.api.dependencies.psycopg2.connect", return_value=mock_conn):
            gen = get_pg()
            conn = next(gen)

        assert conn is mock_conn

    def test_creates_new_connection_when_closed(self, monkeypatch):
        mock_old = MagicMock()
        mock_old.closed = True
        monkeypatch.setattr(dep_module, "_pg_conn", mock_old)

        mock_new = MagicMock()
        with patch("app.api.dependencies.psycopg2.connect", return_value=mock_new):
            gen = get_pg()
            conn = next(gen)

        assert conn is mock_new

    def test_reuses_existing_open_connection(self, monkeypatch):
        mock_conn = MagicMock()
        mock_conn.closed = False
        monkeypatch.setattr(dep_module, "_pg_conn", mock_conn)

        gen = get_pg()
        conn = next(gen)

        assert conn is mock_conn

    def test_reconnects_when_ping_fails(self, monkeypatch):
        mock_old = MagicMock()
        mock_old.closed = False
        mock_old.cursor.return_value.execute.side_effect = Exception("dead")
        monkeypatch.setattr(dep_module, "_pg_conn", mock_old)

        mock_new = MagicMock()
        with patch("app.api.dependencies.psycopg2.connect", return_value=mock_new):
            gen = get_pg()
            conn = next(gen)

        assert conn is mock_new


class TestGetDuck:
    def test_raises_503_when_db_missing(self, monkeypatch, tmp_path):
        missing = tmp_path / "missing.duckdb"
        monkeypatch.setattr(dep_module, "DB_PATH", missing)

        gen = get_duck()
        with pytest.raises(HTTPException) as exc_info:
            next(gen)

        assert exc_info.value.status_code == 503

    def test_yields_connection_when_db_exists(self, monkeypatch, tmp_path):
        db_path = tmp_path / "test.duckdb"
        duckdb.connect(str(db_path)).close()
        monkeypatch.setattr(dep_module, "DB_PATH", db_path)

        gen = get_duck()
        conn = next(gen)

        assert conn is not None
        import contextlib

        with contextlib.suppress(StopIteration):
            next(gen)
