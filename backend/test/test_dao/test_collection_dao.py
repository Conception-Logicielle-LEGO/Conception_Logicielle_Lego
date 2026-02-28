"""
Tests d'intégration pour CollectionDAO (PostgreSQL).

Les fixtures pg_conn, pg_rollback et existing_user
sont définies dans tests/conftest.py.

Lancement :
    pytest test/test_dao/test_collection_dao.py -v
"""

from app.business_object.user_owned_set import UserOwnedSet


# ---------------------------------------------------------------------------
# Tests — add_set_to_collection
# ---------------------------------------------------------------------------


class TestAddSetToCollection:
    def test_add_new_set_returns_user_owned_set(self, dao_collection, existing_user):
        result = dao_collection.add_set_to_collection(existing_user, "42115-1")

        assert isinstance(result, UserOwnedSet)
        assert result.set_num == "42115-1"
        assert result.id_user == existing_user
        assert result.is_built is False

    def test_add_set_with_is_built_true(self, dao_collection, existing_user):
        result = dao_collection.add_set_to_collection(
            existing_user, "10300-1", is_built=True
        )

        assert isinstance(result, UserOwnedSet)
        assert result.is_built is True

    def test_add_duplicate_returns_none(self, dao_collection, existing_user):
        dao_collection.add_set_to_collection(existing_user, "42115-1")
        result = dao_collection.add_set_to_collection(existing_user, "42115-1")

        assert result is None

    def test_add_set_persisted_in_db(self, dao_collection, existing_user, pg_conn):
        dao_collection.add_set_to_collection(existing_user, "42115-1")

        with pg_conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM user_owned_sets WHERE id_user = %s AND set_num = %s",
                (existing_user, "42115-1"),
            )
            row = cur.fetchone()

        assert row is not None
        assert row["set_num"] == "42115-1"

    def test_add_multiple_sets_same_user(self, dao_collection, existing_user):
        dao_collection.add_set_to_collection(existing_user, "42115-1")
        dao_collection.add_set_to_collection(existing_user, "10300-1")

        collection = dao_collection.get_user_collection(existing_user)
        set_nums = [s.set_num for s in collection]

        assert "42115-1" in set_nums
        assert "10300-1" in set_nums


# ---------------------------------------------------------------------------
# Tests — mark_set_as_built
# ---------------------------------------------------------------------------


class TestMarkSetAsBuilt:
    def test_mark_existing_set_returns_true(self, dao_collection, existing_user):
        dao_collection.add_set_to_collection(existing_user, "42115-1")

        result = dao_collection.mark_set_as_built(existing_user, "42115-1")

        assert result is True

    def test_mark_set_updates_is_built_in_db(
        self, dao_collection, existing_user, pg_conn
    ):
        dao_collection.add_set_to_collection(existing_user, "42115-1", is_built=False)
        dao_collection.mark_set_as_built(existing_user, "42115-1")

        with pg_conn.cursor() as cur:
            cur.execute(
                "SELECT is_built FROM user_owned_sets WHERE id_user = %s AND set_num = %s",
                (existing_user, "42115-1"),
            )
            row = cur.fetchone()

        assert row["is_built"] is True

    def test_mark_set_reflected_in_get_collection(self, dao_collection, existing_user):
        """Vérifie la cohérence : après mark, get_user_collection renvoie is_built=True."""
        dao_collection.add_set_to_collection(existing_user, "42115-1", is_built=False)
        dao_collection.mark_set_as_built(existing_user, "42115-1")

        collection = dao_collection.get_user_collection(existing_user)
        owned = next(s for s in collection if s.set_num == "42115-1")

        assert owned.is_built is True

    def test_mark_nonexistent_set_returns_false(self, dao_collection, existing_user):
        result = dao_collection.mark_set_as_built(existing_user, "set_inexistant")

        assert result is False

    def test_mark_already_built_is_idempotent(self, dao_collection, existing_user):
        dao_collection.add_set_to_collection(existing_user, "42115-1", is_built=True)

        result = dao_collection.mark_set_as_built(existing_user, "42115-1")

        assert result is True


# ---------------------------------------------------------------------------
# Tests — get_user_collection
# ---------------------------------------------------------------------------


class TestGetUserCollection:
    def test_empty_collection_returns_empty_list(self, dao_collection, existing_user):
        result = dao_collection.get_user_collection(existing_user)

        assert result == []

    def test_collection_returns_list_of_user_owned_sets(
        self, dao_collection, existing_user
    ):
        dao_collection.add_set_to_collection(existing_user, "42115-1")

        result = dao_collection.get_user_collection(existing_user)

        assert isinstance(result, list)
        assert isinstance(result[0], UserOwnedSet)

    def test_collection_contains_expected_fields(self, dao_collection, existing_user):
        dao_collection.add_set_to_collection(existing_user, "42115-1")

        owned = dao_collection.get_user_collection(existing_user)[0]

        assert owned.set_num == "42115-1"
        assert owned.id_user == existing_user
        assert owned.is_built is False

    def test_collection_ordered_by_acquired_date_desc(
        self, dao_collection, existing_user, pg_conn
    ):
        dao_collection.add_set_to_collection(existing_user, "42115-1")

        # Insère un second set avec une date forcée dans le passé
        with pg_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_owned_sets (id_user, set_num, is_built, acquired_date)
                VALUES (%s, %s, FALSE, '2020-01-01')
                """,
                (existing_user, "10300-1"),
            )

        result = dao_collection.get_user_collection(existing_user)

        assert result[0].set_num == "42115-1"
        assert result[-1].set_num == "10300-1"

    def test_collection_isolation_between_users(
        self, dao_collection, existing_user, pg_conn
    ):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id_user",
                ("other_user", "pw"),
            )
            other_user_id = cur.fetchone()["id_user"]

        dao_collection.add_set_to_collection(existing_user, "42115-1")
        dao_collection.add_set_to_collection(other_user_id, "10300-1")

        result = dao_collection.get_user_collection(existing_user)
        set_nums = [s.set_num for s in result]

        assert "42115-1" in set_nums
        assert "10300-1" not in set_nums


# ---------------------------------------------------------------------------
# Tests — remove_set_from_collection
# ---------------------------------------------------------------------------


class TestRemoveSetFromCollection:
    def test_remove_existing_set_returns_true(self, dao_collection, existing_user):
        dao_collection.add_set_to_collection(existing_user, "42115-1")

        result = dao_collection.remove_set_from_collection(existing_user, "42115-1")

        assert result is True

    def test_remove_set_no_longer_in_collection(self, dao_collection, existing_user):
        dao_collection.add_set_to_collection(existing_user, "42115-1")
        dao_collection.remove_set_from_collection(existing_user, "42115-1")

        result = dao_collection.get_user_collection(existing_user)
        set_nums = [s.set_num for s in result]

        assert "42115-1" not in set_nums

    def test_remove_nonexistent_set_returns_false(self, dao_collection, existing_user):
        result = dao_collection.remove_set_from_collection(
            existing_user, "set_inexistant"
        )

        assert result is False

    def test_remove_only_targets_correct_user(
        self, dao_collection, existing_user, pg_conn
    ):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id_user",
                ("other_user_2", "pw"),
            )
            other_user_id = cur.fetchone()["id_user"]

        dao_collection.add_set_to_collection(existing_user, "42115-1")
        dao_collection.add_set_to_collection(other_user_id, "42115-1")

        dao_collection.remove_set_from_collection(existing_user, "42115-1")

        other_collection = dao_collection.get_user_collection(other_user_id)
        assert any(s.set_num == "42115-1" for s in other_collection)
