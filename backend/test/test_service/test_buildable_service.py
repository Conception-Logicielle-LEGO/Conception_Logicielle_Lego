from unittest.mock import MagicMock, patch

from app.service.buildable_service import BuildableService


def make_service():
    pg_conn = MagicMock()
    duck = MagicMock()
    duck.execute.return_value.fetchall.return_value = []
    duck.description = []
    return pg_conn, duck


# -------------------------
# Test get_buildable_sets
# -------------------------


def test_get_buildable_sets_returns_three_keys():
    pg_conn, duck = make_service()

    with (
        patch("app.service.buildable_service.UserPartsDAO") as mock_user_parts_dao,
        patch("app.service.buildable_service.CollectionDAO") as mock_collection_dao,
    ):
        mock_user_parts_dao.return_value.get_owned_parts.return_value = []
        mock_collection_dao.return_value.get_user_collection.return_value = []

        service = BuildableService(pg_conn=pg_conn, duckdb_conn=duck)
        result = service.get_buildable_sets(user_id=1)

        assert "buildable" in result
        assert "partial" in result
        assert "color_flexible" in result


def test_get_buildable_sets_empty_collection():
    pg_conn, duck = make_service()

    with (
        patch("app.service.buildable_service.UserPartsDAO") as mock_user_parts_dao,
        patch("app.service.buildable_service.CollectionDAO") as mock_collection_dao,
    ):
        mock_user_parts_dao.return_value.get_owned_parts.return_value = []
        mock_collection_dao.return_value.get_user_collection.return_value = []

        service = BuildableService(pg_conn=pg_conn, duckdb_conn=duck)
        result = service.get_buildable_sets(user_id=1)

        assert result["buildable"] == []
        assert result["partial"] == []
        assert result["color_flexible"] == []


def test_load_user_stock_with_unbuilt_sets():
    """Couvre les lignes 126-141 : sets non construits dans la collection."""
    pg_conn = MagicMock()
    duck = MagicMock()

    fake_set = MagicMock()
    fake_set.set_num = "1234-1"
    fake_set.is_built = False

    # Séquence des appels duck.execute() dans _load_user_stock puis les 3 requêtes
    unbuilt_result = MagicMock()
    unbuilt_result.fetchall.return_value = [("3001", 4, 2)]
    empty_result = MagicMock()
    empty_result.fetchall.return_value = []

    duck.execute.side_effect = [
        unbuilt_result,  # requête pièces des sets non construits
        MagicMock(),  # CREATE TEMP TABLE
        MagicMock(),  # DELETE FROM _user_parts
        empty_result,  # _query_buildable
        empty_result,  # _query_partial
        empty_result,  # _query_color_flexible
    ]
    duck.description = [("part_num",), ("color_id",), ("qty",)]

    with (
        patch("app.service.buildable_service.UserPartsDAO") as mock_user_parts_dao,
        patch("app.service.buildable_service.CollectionDAO") as mock_collection_dao,
    ):
        mock_user_parts_dao.return_value.get_owned_parts.return_value = []
        mock_collection_dao.return_value.get_user_collection.return_value = [fake_set]

        service = BuildableService(pg_conn=pg_conn, duckdb_conn=duck)
        service.get_buildable_sets(user_id=1)

        duck.executemany.assert_called_once()  # owned_parts non vide → executemany appelé


def test_load_user_stock_with_owned_parts():
    """Couvre la ligne 150 : executemany quand l'utilisateur possède des pièces."""
    pg_conn = MagicMock()
    duck = MagicMock()
    duck.execute.return_value.fetchall.return_value = []
    duck.description = []

    with (
        patch("app.service.buildable_service.UserPartsDAO") as mock_user_parts_dao,
        patch("app.service.buildable_service.CollectionDAO") as mock_collection_dao,
    ):
        mock_user_parts_dao.return_value.get_owned_parts.return_value = [
            {"part_num": "3001", "color_id": 4, "quantity": 2}
        ]
        mock_collection_dao.return_value.get_user_collection.return_value = []

        service = BuildableService(pg_conn=pg_conn, duckdb_conn=duck)
        service.get_buildable_sets(user_id=1)

        duck.executemany.assert_called_once()


# -------------------------
# Test _make_exclude
# -------------------------


def test_make_exclude_empty():
    pg_conn, duck = make_service()

    with (
        patch("app.service.buildable_service.UserPartsDAO"),
        patch("app.service.buildable_service.CollectionDAO"),
    ):
        service = BuildableService(pg_conn=pg_conn, duckdb_conn=duck)
        sql, params = service._make_exclude([])
        assert sql == "NULL"
        assert params == []


def test_make_exclude_with_values():
    pg_conn, duck = make_service()

    with (
        patch("app.service.buildable_service.UserPartsDAO"),
        patch("app.service.buildable_service.CollectionDAO"),
    ):
        service = BuildableService(pg_conn=pg_conn, duckdb_conn=duck)
        sql, params = service._make_exclude(["1234-1", "5678-1"])
        assert sql == "?, ?"
        assert params == ["1234-1", "5678-1"]
