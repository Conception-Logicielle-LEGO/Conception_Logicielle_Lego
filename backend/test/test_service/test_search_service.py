from unittest.mock import MagicMock

from app.service.search_service import SearchService


def make_service():
    dao = MagicMock()
    return SearchService(dao=dao), dao


# -------------------------
# Test search_sets
# -------------------------

def test_search_sets():
    service, dao = make_service()
    dao.search_sets.return_value = [{"set_num": "1234-1", "name": "Castle"}]
    result = service.search_sets(query="castle", theme_id=1, year_from=2000, year_to=2020, limit=10)
    dao.search_sets.assert_called_once_with("castle", 1, 2000, 2020, 10)
    assert len(result) == 1


# -------------------------
# Test search_parts
# -------------------------

def test_search_parts():
    service, dao = make_service()
    dao.search_parts.return_value = [{"part_num": "3001", "name": "Brick"}]
    result = service.search_parts(query="brick", color_id=4, category_id=2, limit=5)
    dao.search_parts.assert_called_once_with("brick", 4, 2, 5)
    assert len(result) == 1


# -------------------------
# Test get_recent_sets
# -------------------------

def test_get_recent_sets():
    service, dao = make_service()
    dao.get_recent_sets.return_value = [{"set_num": "9999-1"}]
    result = service.get_recent_sets(limit=12)
    dao.get_recent_sets.assert_called_once_with(12)
    assert result == [{"set_num": "9999-1"}]


# -------------------------
# Test get_stats
# -------------------------

def test_get_stats():
    service, dao = make_service()
    dao.get_stats.return_value = {"total_sets": 1000, "total_parts": 50000}
    result = service.get_stats()
    dao.get_stats.assert_called_once()
    assert result["total_sets"] == 1000
