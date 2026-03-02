"""
Tests d'intégration pour WishlistDAO (PostgreSQL).

Lancement :
    pytest test/test_dao/test_wishlist_dao.py -v
"""


# ---------------------------------------------------------------------------
# Tests — get_or_create_wishlist
# ---------------------------------------------------------------------------


class TestGetOrCreateWishlist:
    def test_creates_wishlist_for_new_user(self, dao_wishlist, existing_user):
        wishlist_id = dao_wishlist.get_or_create_wishlist(existing_user)

        assert isinstance(wishlist_id, int)
        assert wishlist_id > 0

    def test_returns_same_id_for_existing_wishlist(self, dao_wishlist, existing_user):
        id1 = dao_wishlist.get_or_create_wishlist(existing_user)
        id2 = dao_wishlist.get_or_create_wishlist(existing_user)

        assert id1 == id2


# ---------------------------------------------------------------------------
# Tests — add_set / remove_set / get_sets
# ---------------------------------------------------------------------------


class TestWishlistSets:
    def test_add_set_returns_dict(self, dao_wishlist, existing_user):
        result = dao_wishlist.add_set(existing_user, "75192-1")

        assert result is not None
        assert result["set_num"] == "75192-1"

    def test_add_duplicate_set_returns_none(self, dao_wishlist, existing_user):
        dao_wishlist.add_set(existing_user, "75192-1")
        result = dao_wishlist.add_set(existing_user, "75192-1")

        assert result is None

    def test_get_sets_returns_added_sets(self, dao_wishlist, existing_user):
        dao_wishlist.add_set(existing_user, "75192-1")
        dao_wishlist.add_set(existing_user, "10276-1")

        sets = dao_wishlist.get_sets(existing_user)
        set_nums = [s["set_num"] for s in sets]

        assert "75192-1" in set_nums
        assert "10276-1" in set_nums

    def test_get_sets_empty_returns_empty_list(self, dao_wishlist, existing_user):
        result = dao_wishlist.get_sets(existing_user)

        assert result == []

    def test_remove_set_returns_true(self, dao_wishlist, existing_user):
        dao_wishlist.add_set(existing_user, "75192-1")
        result = dao_wishlist.remove_set(existing_user, "75192-1")

        assert result is True

    def test_remove_nonexistent_set_returns_false(self, dao_wishlist, existing_user):
        result = dao_wishlist.remove_set(existing_user, "set_inexistant")

        assert result is False

    def test_remove_set_no_longer_in_list(self, dao_wishlist, existing_user):
        dao_wishlist.add_set(existing_user, "75192-1")
        dao_wishlist.remove_set(existing_user, "75192-1")

        sets = dao_wishlist.get_sets(existing_user)
        assert not any(s["set_num"] == "75192-1" for s in sets)


# ---------------------------------------------------------------------------
# Tests — add_part / remove_part / get_parts
# ---------------------------------------------------------------------------


class TestWishlistParts:
    def test_add_part_returns_dict(self, dao_wishlist, existing_user):
        result = dao_wishlist.add_part(existing_user, "3001", 1, 2)

        assert result is not None
        assert result["part_num"] == "3001"
        assert result["quantity"] == 2

    def test_add_duplicate_part_updates_quantity(self, dao_wishlist, existing_user):
        dao_wishlist.add_part(existing_user, "3001", 1, 2)
        result = dao_wishlist.add_part(existing_user, "3001", 1, 5)

        assert result["quantity"] == 5

    def test_get_parts_returns_added_parts(self, dao_wishlist, existing_user):
        dao_wishlist.add_part(existing_user, "3001", 1, 1)
        dao_wishlist.add_part(existing_user, "3002", 2, 3)

        parts = dao_wishlist.get_parts(existing_user)
        part_nums = [p["part_num"] for p in parts]

        assert "3001" in part_nums
        assert "3002" in part_nums

    def test_get_parts_empty_returns_empty_list(self, dao_wishlist, existing_user):
        result = dao_wishlist.get_parts(existing_user)

        assert result == []

    def test_remove_part_returns_true(self, dao_wishlist, existing_user):
        dao_wishlist.add_part(existing_user, "3001", 1, 1)
        result = dao_wishlist.remove_part(existing_user, "3001", 1)

        assert result is True

    def test_remove_nonexistent_part_returns_false(self, dao_wishlist, existing_user):
        result = dao_wishlist.remove_part(existing_user, "part_inexistant", 999)

        assert result is False

    def test_remove_part_no_longer_in_list(self, dao_wishlist, existing_user):
        dao_wishlist.add_part(existing_user, "3001", 1, 1)
        dao_wishlist.remove_part(existing_user, "3001", 1)

        parts = dao_wishlist.get_parts(existing_user)
        assert not any(p["part_num"] == "3001" for p in parts)
