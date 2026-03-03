"""Tests pour SearchDAO (DuckDB, LIKE fallback et chemins VSS)."""

import pytest
from unittest.mock import MagicMock, patch

import app.database.dao.search_dao as search_module
from app.database.dao.search_dao import SearchDAO, _has_embeddings, _has_vss


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SET_COLS = [("set_num",), ("name",), ("year",), ("theme_id",), ("num_parts",), ("img_url",)]
PART_COLS = [("part_num",), ("name",), ("part_cat_id",), ("img_url",)]


def make_mock_conn(cols=SET_COLS, rows=None):
    """Crée un mock DuckDB qui ne lève pas et renvoie les lignes demandées."""
    mock_conn = MagicMock()
    mock_conn.description = cols
    mock_conn.execute.return_value.fetchall.return_value = rows or []
    mock_conn.execute.return_value.fetchone.return_value = (0,)
    return mock_conn


# ---------------------------------------------------------------------------
# Tests fonctions module-level
# ---------------------------------------------------------------------------


class TestHasEmbeddings:
    def test_returns_true_when_execute_succeeds(self):
        mock_conn = MagicMock()
        assert _has_embeddings(mock_conn) is True

    def test_returns_false_when_execute_raises(self):
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = Exception("table not found")
        assert _has_embeddings(mock_conn) is False


class TestHasVss:
    def test_returns_true_when_load_succeeds(self):
        mock_conn = MagicMock()
        assert _has_vss(mock_conn) is True

    def test_returns_false_when_load_raises(self):
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = Exception("vss not available")
        assert _has_vss(mock_conn) is False


# ---------------------------------------------------------------------------
# Tests SearchDAO — chemin LIKE (_st_model = None)
# ---------------------------------------------------------------------------


class TestSearchSetsLike:
    def setup_method(self):
        self.patcher = patch.object(search_module, "_st_model", None)
        self.patcher.start()

    def teardown_method(self):
        self.patcher.stop()

    def test_search_sets_returns_list(self):
        mock_conn = make_mock_conn(SET_COLS, [("1234-1", "Castle", 2023, 1, 100, "img")])
        dao = SearchDAO(mock_conn)
        result = dao.search_sets("castle")
        assert len(result) == 1
        assert result[0]["set_num"] == "1234-1"

    def test_search_sets_empty_query(self):
        mock_conn = make_mock_conn(SET_COLS, [])
        dao = SearchDAO(mock_conn)
        result = dao.search_sets("")
        assert result == []

    def test_search_sets_with_all_filters(self):
        mock_conn = make_mock_conn(SET_COLS, [])
        dao = SearchDAO(mock_conn)
        result = dao.search_sets("castle", theme_id=1, year_from=2020, year_to=2023, limit=5)
        assert isinstance(result, list)

    def test_search_sets_with_no_query(self):
        mock_conn = make_mock_conn(SET_COLS, [("1234-1", "Castle", 2023, 1, 100, "img")])
        dao = SearchDAO(mock_conn)
        result = dao.search_sets("", theme_id=1)
        assert isinstance(result, list)


class TestSearchPartsLike:
    def setup_method(self):
        self.patcher = patch.object(search_module, "_st_model", None)
        self.patcher.start()

    def teardown_method(self):
        self.patcher.stop()

    def test_search_parts_returns_list(self):
        mock_conn = make_mock_conn(PART_COLS, [("3001", "Brick", 1, "img")])
        dao = SearchDAO(mock_conn)
        result = dao.search_parts("brick")
        assert len(result) == 1
        assert result[0]["part_num"] == "3001"

    def test_search_parts_with_category_filter(self):
        mock_conn = make_mock_conn(PART_COLS, [])
        dao = SearchDAO(mock_conn)
        result = dao.search_parts("brick", category_id=5)
        assert isinstance(result, list)

    def test_search_parts_empty_query(self):
        mock_conn = make_mock_conn(PART_COLS, [])
        dao = SearchDAO(mock_conn)
        result = dao.search_parts("")
        assert result == []


class TestGetRecentSetsAndStats:
    def setup_method(self):
        self.patcher = patch.object(search_module, "_st_model", None)
        self.patcher.start()

    def teardown_method(self):
        self.patcher.stop()

    def test_get_recent_sets(self):
        mock_conn = make_mock_conn(SET_COLS, [("1234-1", "Castle", 2023, 1, 100, "img")])
        dao = SearchDAO(mock_conn)
        result = dao.get_recent_sets()
        assert len(result) == 1

    def test_get_stats(self):
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.side_effect = [(100,), (200,), (50,)]
        dao = SearchDAO(mock_conn)
        stats = dao.get_stats()
        assert stats["totalSets"] == 100
        assert stats["totalParts"] == 200
        assert stats["totalThemes"] == 50


# ---------------------------------------------------------------------------
# Tests SearchDAO — chemin VSS (_st_model mocké)
# ---------------------------------------------------------------------------


class TestSearchSetsVss:
    def test_search_sets_vss_path(self):
        mock_model = MagicMock()
        mock_vec = MagicMock()
        mock_vec.tolist.return_value = [0.1] * 384
        mock_model.embed.return_value = iter([mock_vec])

        with patch.object(search_module, "_st_model", mock_model):
            vss_cols = SET_COLS + [("distance",)]
            mock_conn = make_mock_conn(
                vss_cols, [("1234-1", "Castle", 2023, 1, 100, "img", 0.1)]
            )
            dao = SearchDAO(mock_conn)
            dao._encode = MagicMock(return_value=[0.1] * 384)
            result = dao.search_sets("castle")

        assert len(result) == 1

    def test_search_sets_vss_with_filters(self):
        mock_model = MagicMock()

        with patch.object(search_module, "_st_model", mock_model):
            vss_cols = SET_COLS + [("distance",)]
            mock_conn = make_mock_conn(vss_cols, [])
            dao = SearchDAO(mock_conn)
            dao._encode = MagicMock(return_value=[0.1] * 384)
            result = dao.search_sets("castle", theme_id=1, year_from=2020, year_to=2023)

        assert isinstance(result, list)


class TestSearchPartsVss:
    def test_search_parts_vss_path(self):
        mock_model = MagicMock()

        with patch.object(search_module, "_st_model", mock_model):
            vss_cols = PART_COLS + [("distance",)]
            mock_conn = make_mock_conn(vss_cols, [("3001", "Brick", 1, "img", 0.1)])
            dao = SearchDAO(mock_conn)
            dao._encode = MagicMock(return_value=[0.1] * 384)
            result = dao.search_parts("brick")

        assert len(result) == 1

    def test_search_parts_vss_with_color_and_category(self):
        mock_model = MagicMock()

        with patch.object(search_module, "_st_model", mock_model):
            vss_cols = PART_COLS + [("distance",)]
            mock_conn = make_mock_conn(vss_cols, [])
            dao = SearchDAO(mock_conn)
            dao._encode = MagicMock(return_value=[0.1] * 384)
            result = dao.search_parts("brick", color_id=4, category_id=5)

        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Test _encode — RuntimeError si _st_model est None
# ---------------------------------------------------------------------------


def test_encode_raises_when_no_model():
    with patch.object(search_module, "_st_model", None):
        mock_conn = make_mock_conn()
        dao = SearchDAO(mock_conn)

        with pytest.raises(RuntimeError, match="fastembed"):
            dao._encode("test query")


def test_encode_returns_vector_with_model():
    mock_model = MagicMock()
    mock_vec = MagicMock()
    mock_vec.tolist.return_value = [0.1] * 384
    mock_model.embed.return_value = iter([mock_vec])

    with patch.object(search_module, "_st_model", mock_model):
        mock_conn = make_mock_conn()
        dao = SearchDAO(mock_conn)
        result = dao._encode("test query")

    assert len(result) == 384
