"""
Tests d'intégration pour UserPartsDAO (PostgreSQL).

Lancement :
    pytest test/test_dao/test_user_parts_dao.py -v
"""


# ---------------------------------------------------------------------------
# Tests — add_part
# ---------------------------------------------------------------------------


class TestAddPart:
    def test_add_new_part_returns_dict(self, dao_user_parts, existing_user):
        result = dao_user_parts.add_part(existing_user, "3001", 1, "owned", 2)

        assert result is not None
        assert result["part_num"] == "3001"
        assert result["color_id"] == 1
        assert result["quantity"] == 2
        assert result["status"] == "owned"

    def test_add_duplicate_accumulates_quantity(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 3)
        result = dao_user_parts.add_part(existing_user, "3001", 1, "owned", 2)

        assert result["quantity"] == 5

    def test_add_libre_and_used_tracked_separately(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 5, is_used=False)
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 2, is_used=True)

        owned = dao_user_parts.get_owned_parts(existing_user)
        assert len(owned) == 2
        libre = next(r for r in owned if not r["is_used"])
        used = next(r for r in owned if r["is_used"])
        assert libre["quantity"] == 5
        assert used["quantity"] == 2

    def test_add_wished_part(self, dao_user_parts, existing_user):
        result = dao_user_parts.add_part(existing_user, "3001", 1, "wished", 1)

        assert result["status"] == "wished"

    def test_add_part_persisted(self, dao_user_parts, existing_user, pg_conn):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 4)

        with pg_conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM user_parts WHERE id_user = %s AND part_num = %s",
                (existing_user, "3001"),
            )
            row = cur.fetchone()

        assert row is not None
        assert row["quantity"] == 4


# ---------------------------------------------------------------------------
# Tests — remove_part
# ---------------------------------------------------------------------------


class TestRemovePart:
    def test_remove_existing_part_returns_true(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 1)
        result = dao_user_parts.remove_part(existing_user, "3001", 1)

        assert result is True

    def test_remove_nonexistent_part_returns_false(self, dao_user_parts, existing_user):
        result = dao_user_parts.remove_part(existing_user, "part_inexistant", 999)

        assert result is False

    def test_remove_part_no_longer_in_db(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 1)
        dao_user_parts.remove_part(existing_user, "3001", 1)

        parts = dao_user_parts.get_owned_parts(existing_user)
        assert not any(p["part_num"] == "3001" for p in parts)


# ---------------------------------------------------------------------------
# Tests — get_owned_parts
# ---------------------------------------------------------------------------


class TestGetOwnedParts:
    def test_empty_returns_empty_list(self, dao_user_parts, existing_user):
        result = dao_user_parts.get_owned_parts(existing_user)

        assert result == []

    def test_returns_only_owned_parts(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 2)
        dao_user_parts.add_part(existing_user, "3002", 1, "wished", 1)

        owned = dao_user_parts.get_owned_parts(existing_user)

        assert len(owned) == 1
        assert owned[0]["part_num"] == "3001"

    def test_returns_list_of_dicts(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 1)

        result = dao_user_parts.get_owned_parts(existing_user)

        assert isinstance(result, list)
        assert isinstance(result[0], dict)


# ---------------------------------------------------------------------------
# Tests — get_wished_parts
# ---------------------------------------------------------------------------


class TestGetWishedParts:
    def test_returns_only_wished_parts(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 2)
        dao_user_parts.add_part(existing_user, "3002", 1, "wished", 1)

        wished = dao_user_parts.get_wished_parts(existing_user)

        assert len(wished) == 1
        assert wished[0]["part_num"] == "3002"


# ---------------------------------------------------------------------------
# Tests — update_quantity
# ---------------------------------------------------------------------------


class TestUpdateQuantity:
    def test_update_existing_quantity(self, dao_user_parts, existing_user):
        dao_user_parts.add_part(existing_user, "3001", 1, "owned", 5)
        result = dao_user_parts.update_quantity(existing_user, "3001", 1, 10)

        assert result is True
        owned = dao_user_parts.get_owned_parts(existing_user)
        assert owned[0]["quantity"] == 10

    def test_update_nonexistent_returns_false(self, dao_user_parts, existing_user):
        result = dao_user_parts.update_quantity(existing_user, "inexistant", 999, 5)

        assert result is False
