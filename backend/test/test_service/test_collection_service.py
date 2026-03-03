from unittest.mock import MagicMock

from app.service.collection_service import CollectionService


def make_service():
    dao = MagicMock()
    conn = MagicMock()
    return CollectionService(dao=dao, pg_conn=conn), dao, conn


# -------------------------
# Test get_collection
# -------------------------

def test_get_collection():
    service, dao, _ = make_service()
    dao.get_user_collection.return_value = ["set1", "set2"]
    result = service.get_collection(user_id=1)
    dao.get_user_collection.assert_called_once_with(1)
    assert result == ["set1", "set2"]


# -------------------------
# Test add_set
# -------------------------

def test_add_set_success():
    service, dao, conn = make_service()
    dao.add_set_to_collection.return_value = {"set_num": "1234-1"}
    result = service.add_set(user_id=1, set_num="1234-1")
    dao.add_set_to_collection.assert_called_once_with(1, "1234-1", False)
    conn.commit.assert_called_once()
    assert result is not None


def test_add_set_doublon():
    service, dao, conn = make_service()
    dao.add_set_to_collection.return_value = None
    result = service.add_set(user_id=1, set_num="1234-1")
    conn.commit.assert_not_called()
    assert result is None


# -------------------------
# Test remove_set
# -------------------------

def test_remove_set():
    service, dao, conn = make_service()
    dao.remove_set_from_collection.return_value = True
    result = service.remove_set(user_id=1, set_num="1234-1")
    dao.remove_set_from_collection.assert_called_once_with(1, "1234-1")
    conn.commit.assert_called_once()
    assert result is True


# -------------------------
# Test mark_built
# -------------------------

def test_mark_built_true():
    service, dao, conn = make_service()
    dao.mark_set_as_built.return_value = True
    result = service.mark_built(user_id=1, set_num="1234-1", is_built=True)
    dao.mark_set_as_built.assert_called_once_with(1, "1234-1")
    conn.commit.assert_called_once()
    assert result is True


def test_mark_built_false():
    service, dao, conn = make_service()
    dao.mark_set_as_unbuilt.return_value = True
    result = service.mark_built(user_id=1, set_num="1234-1", is_built=False)
    dao.mark_set_as_unbuilt.assert_called_once_with(1, "1234-1")
    conn.commit.assert_called_once()
    assert result is True


def test_mark_built_not_updated():
    service, dao, conn = make_service()
    dao.mark_set_as_built.return_value = False
    result = service.mark_built(user_id=1, set_num="1234-1", is_built=True)
    conn.commit.assert_not_called()
    assert result is False
