from unittest.mock import MagicMock

from app.service.wishlist_service import WishlistService


def make_service():
    dao = MagicMock()
    conn = MagicMock()
    return WishlistService(dao=dao, pg_conn=conn), dao, conn


# -------------------------
# Test sets
# -------------------------


def test_add_set():
    service, dao, conn = make_service()
    dao.add_set.return_value = True
    result = service.add_set(user_id=1, set_num="1234-1")
    dao.add_set.assert_called_once_with(1, "1234-1", 0)
    conn.commit.assert_called_once()
    assert result is True


def test_remove_set():
    service, dao, conn = make_service()
    dao.remove_set.return_value = True
    result = service.remove_set(user_id=1, set_num="1234-1")
    dao.remove_set.assert_called_once_with(1, "1234-1")
    conn.commit.assert_called_once()
    assert result is True


def test_get_sets():
    service, dao, _ = make_service()
    dao.get_sets.return_value = [{"set_num": "1234-1"}]
    result = service.get_sets(user_id=1)
    dao.get_sets.assert_called_once_with(1)
    assert result == [{"set_num": "1234-1"}]


# -------------------------
# Test parts
# -------------------------


def test_add_part():
    service, dao, conn = make_service()
    dao.add_part.return_value = True
    result = service.add_part(user_id=1, part_num="3001", color_id=4)
    dao.add_part.assert_called_once_with(1, "3001", 4, 1)
    conn.commit.assert_called_once()
    assert result is True


def test_remove_part():
    service, dao, conn = make_service()
    dao.remove_part.return_value = True
    result = service.remove_part(user_id=1, part_num="3001", color_id=4)
    dao.remove_part.assert_called_once_with(1, "3001", 4)
    conn.commit.assert_called_once()
    assert result is True


def test_get_parts():
    service, dao, _ = make_service()
    dao.get_parts.return_value = [{"part_num": "3001"}]
    result = service.get_parts(user_id=1)
    dao.get_parts.assert_called_once_with(1)
    assert result == [{"part_num": "3001"}]


def test_update_part_quantity_success():
    service, dao, conn = make_service()
    dao.update_part_quantity.return_value = True
    result = service.update_part_quantity(1, "3001", 4, 3)
    dao.update_part_quantity.assert_called_once_with(1, "3001", 4, 3)
    conn.commit.assert_called_once()
    assert result is True


def test_update_part_quantity_not_found():
    service, dao, conn = make_service()
    dao.update_part_quantity.return_value = False
    result = service.update_part_quantity(1, "9999", 4, 3)
    conn.commit.assert_called_once()
    assert result is False
