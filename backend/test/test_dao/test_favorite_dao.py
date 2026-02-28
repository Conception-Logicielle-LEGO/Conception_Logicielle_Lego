"""
Tests d'intégration pour FavoriteDAO (PostgreSQL).

Les fixtures pg_conn, pg_rollback et existing_user
sont définies dans test/conftest.py.

Lancement :
    pytest test/test_dao/test_favorite_dao.py -v
"""

import pytest

from app.business_object.favorite_set import FavoriteSet
from app.database.dao.favorite_dao import FavoriteDAO


@pytest.fixture()
def dao(pg_conn):
    return FavoriteDAO(pg_conn)


# ---------------------------------------------------------------------------
# Tests — add_favorite
# ---------------------------------------------------------------------------


class TestAddFavorite:
    def test_add_new_favorite_returns_favorite_set(self, dao, existing_user):
        result = dao.add_favorite(existing_user, "42115-1")

        assert isinstance(result, FavoriteSet)
        assert result.set_num == "42115-1"
        assert result.id_user == existing_user
        assert result.added_at is not None

    def test_add_duplicate_returns_none(self, dao, existing_user):
        dao.add_favorite(existing_user, "42115-1")
        result = dao.add_favorite(existing_user, "42115-1")

        assert result is None

    def test_add_favorite_persisted_in_db(self, dao, existing_user, pg_conn):
        dao.add_favorite(existing_user, "42115-1")

        with pg_conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM favorite_sets WHERE id_user = %s AND set_num = %s",
                (existing_user, "42115-1"),
            )
            row = cur.fetchone()

        assert row is not None
        assert row["set_num"] == "42115-1"

    def test_add_multiple_favorites_same_user(self, dao, existing_user):
        dao.add_favorite(existing_user, "42115-1")
        dao.add_favorite(existing_user, "10300-1")

        favorites = dao.get_user_favorites(existing_user)
        set_nums = [f.set_num for f in favorites]

        assert "42115-1" in set_nums
        assert "10300-1" in set_nums


# ---------------------------------------------------------------------------
# Tests — remove_favorite
# ---------------------------------------------------------------------------


class TestRemoveFavorite:
    def test_remove_existing_favorite_returns_true(self, dao, existing_user):
        dao.add_favorite(existing_user, "42115-1")

        result = dao.remove_favorite(existing_user, "42115-1")

        assert result is True

    def test_remove_favorite_no_longer_in_list(self, dao, existing_user):
        dao.add_favorite(existing_user, "42115-1")
        dao.remove_favorite(existing_user, "42115-1")

        favorites = dao.get_user_favorites(existing_user)
        set_nums = [f.set_num for f in favorites]

        assert "42115-1" not in set_nums

    def test_remove_nonexistent_favorite_returns_false(self, dao, existing_user):
        result = dao.remove_favorite(existing_user, "set_inexistant")

        assert result is False

    def test_remove_only_targets_correct_user(self, dao, existing_user, pg_conn):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id_user",
                ("other_user", "pw"),
            )
            other_user_id = cur.fetchone()["id_user"]

        dao.add_favorite(existing_user, "42115-1")
        dao.add_favorite(other_user_id, "42115-1")

        dao.remove_favorite(existing_user, "42115-1")

        other_favorites = dao.get_user_favorites(other_user_id)
        assert any(f.set_num == "42115-1" for f in other_favorites)


# ---------------------------------------------------------------------------
# Tests — get_user_favorites
# ---------------------------------------------------------------------------


class TestGetUserFavorites:
    def test_empty_favorites_returns_empty_list(self, dao, existing_user):
        result = dao.get_user_favorites(existing_user)

        assert result == []

    def test_favorites_returns_list_of_favorite_sets(self, dao, existing_user):
        dao.add_favorite(existing_user, "42115-1")

        result = dao.get_user_favorites(existing_user)

        assert isinstance(result, list)
        assert isinstance(result[0], FavoriteSet)

    def test_favorites_contains_expected_fields(self, dao, existing_user):
        dao.add_favorite(existing_user, "42115-1")

        fav = dao.get_user_favorites(existing_user)[0]

        assert fav.set_num == "42115-1"
        assert fav.id_user == existing_user
        assert fav.added_at is not None

    def test_favorites_ordered_by_added_at_desc(self, dao, existing_user, pg_conn):
        dao.add_favorite(existing_user, "42115-1")

        with pg_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO favorite_sets (id_user, set_num, added_at)
                VALUES (%s, %s, '2020-01-01')
                """,
                (existing_user, "10300-1"),
            )

        result = dao.get_user_favorites(existing_user)

        assert result[0].set_num == "42115-1"
        assert result[-1].set_num == "10300-1"

    def test_favorites_isolation_between_users(self, dao, existing_user, pg_conn):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id_user",
                ("other_user", "pw"),
            )
            other_user_id = cur.fetchone()["id_user"]

        dao.add_favorite(existing_user, "42115-1")
        dao.add_favorite(other_user_id, "10300-1")

        result = dao.get_user_favorites(existing_user)
        set_nums = [f.set_num for f in result]

        assert "42115-1" in set_nums
        assert "10300-1" not in set_nums
