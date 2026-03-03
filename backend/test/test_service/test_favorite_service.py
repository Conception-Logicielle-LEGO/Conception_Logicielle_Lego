from unittest.mock import MagicMock

from app.service.favorite_service import FavoriteService


def make_service():
    dao = MagicMock()
    conn = MagicMock()
    return FavoriteService(dao=dao, pg_conn=conn), dao, conn


# -------------------------
# Test get_favorites
# -------------------------


def test_get_favorites():
    service, dao, _ = make_service()
    dao.get_user_favorites.return_value = [{"set_num": "1234-1"}]
    result = service.get_favorites(user_id=1)
    dao.get_user_favorites.assert_called_once_with(1)
    assert result == [{"set_num": "1234-1"}]


# -------------------------
# Test add_favorite
# -------------------------


def test_add_favorite_success():
    service, dao, conn = make_service()
    dao.add_favorite.return_value = {"set_num": "1234-1"}
    result = service.add_favorite(user_id=1, set_num="1234-1")
    dao.add_favorite.assert_called_once_with(1, "1234-1")
    conn.commit.assert_called_once()
    assert result is not None


def test_add_favorite_doublon():
    service, dao, conn = make_service()
    dao.add_favorite.return_value = None
    result = service.add_favorite(user_id=1, set_num="1234-1")
    conn.commit.assert_not_called()
    assert result is None


# -------------------------
# Test remove_favorite
# -------------------------


def test_remove_favorite():
    service, dao, conn = make_service()
    dao.remove_favorite.return_value = True
    result = service.remove_favorite(user_id=1, set_num="1234-1")
    dao.remove_favorite.assert_called_once_with(1, "1234-1")
    conn.commit.assert_called_once()
    assert result is True
