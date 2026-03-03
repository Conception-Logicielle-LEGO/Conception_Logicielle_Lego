from unittest.mock import MagicMock

from app.service.user_parts_service import UserPartsService


def make_service():
    dao = MagicMock()
    conn = MagicMock()
    return UserPartsService(dao=dao, pg_conn=conn), dao, conn


# -------------------------
# Test add_part
# -------------------------

def test_add_part():
    service, dao, conn = make_service()
    dao.add_part.return_value = True
    result = service.add_part(user_id=1, part_num="3001", color_id=4, quantity=2)
    dao.add_part.assert_called_once_with(1, "3001", 4, "owned", 2, False)
    conn.commit.assert_called_once()
    assert result is True


# -------------------------
# Test remove_part
# -------------------------

def test_remove_part():
    service, dao, conn = make_service()
    dao.remove_part.return_value = True
    result = service.remove_part(user_id=1, part_num="3001", color_id=4)
    dao.remove_part.assert_called_once_with(1, "3001", 4)
    conn.commit.assert_called_once()
    assert result is True


# -------------------------
# Test update_quantity
# -------------------------

def test_update_quantity():
    service, dao, conn = make_service()
    dao.update_quantity.return_value = True
    result = service.update_quantity(user_id=1, part_num="3001", color_id=4, quantity=5)
    dao.update_quantity.assert_called_once_with(1, "3001", 4, 5)
    conn.commit.assert_called_once()
    assert result is True


# -------------------------
# Test get_owned_parts
# -------------------------

def test_get_owned_parts():
    service, dao, _ = make_service()
    dao.get_owned_parts.return_value = [{"part_num": "3001", "quantity": 2}]
    result = service.get_owned_parts(user_id=1)
    dao.get_owned_parts.assert_called_once_with(1)
    assert result == [{"part_num": "3001", "quantity": 2}]


# -------------------------
# Test get_wished_parts
# -------------------------

def test_get_wished_parts():
    service, dao, _ = make_service()
    dao.get_wished_parts.return_value = [{"part_num": "3002", "quantity": 1}]
    result = service.get_wished_parts(user_id=1)
    dao.get_wished_parts.assert_called_once_with(1)
    assert result == [{"part_num": "3002", "quantity": 1}]
