"""Tests pour BaseDAO (méthodes génériques get_by, get_all, exists)."""

import pytest
from unittest.mock import MagicMock

from app.database.dao.base_dao import BaseDAO


class ConcreteDAO(BaseDAO):
    """Sous-classe concrète pour tester BaseDAO."""

    def get_table_name(self) -> str:
        return "test_table"

    def get_allowed_columns(self) -> set[str]:
        return {"id", "name"}

    def from_row(self, row: dict):
        return row


def make_dao():
    mock_conn = MagicMock()
    mock_factory = MagicMock(return_value=mock_conn)
    dao = ConcreteDAO(mock_factory)
    return dao, mock_conn


class TestGetBy:
    def test_get_by_valid_column_returns_rows(self):
        dao, mock_conn = make_dao()
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": 1, "name": "brick"}
        ]

        result = dao.get_by("id", 1)

        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_get_by_invalid_column_raises_value_error(self):
        dao, _ = make_dao()

        with pytest.raises(ValueError, match="non autorisée"):
            dao.get_by("bad_col", "value")

    def test_get_by_empty_result(self):
        dao, mock_conn = make_dao()
        mock_conn.execute.return_value.fetchall.return_value = []

        result = dao.get_by("name", "unknown")

        assert result == []


class TestGetAll:
    def test_get_all_returns_all_rows(self):
        dao, mock_conn = make_dao()
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": 1, "name": "a"},
            {"id": 2, "name": "b"},
        ]

        result = dao.get_all()

        assert len(result) == 2

    def test_get_all_empty_table(self):
        dao, mock_conn = make_dao()
        mock_conn.execute.return_value.fetchall.return_value = []

        result = dao.get_all()

        assert result == []


class TestExists:
    def test_exists_true_when_count_greater_than_zero(self):
        dao, mock_conn = make_dao()
        mock_conn.execute.return_value.fetchone.return_value = {"count": 1}

        assert dao.exists("id", 1) is True

    def test_exists_false_when_count_zero(self):
        dao, mock_conn = make_dao()
        mock_conn.execute.return_value.fetchone.return_value = {"count": 0}

        assert dao.exists("id", 999) is False

    def test_exists_false_when_fetchone_returns_none(self):
        dao, mock_conn = make_dao()
        mock_conn.execute.return_value.fetchone.return_value = None

        assert dao.exists("id", 999) is False

    def test_exists_invalid_column_raises_value_error(self):
        dao, _ = make_dao()

        with pytest.raises(ValueError):
            dao.exists("bad_col", "value")
