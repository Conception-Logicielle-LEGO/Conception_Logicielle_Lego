from unittest.mock import patch


# -------------------------
# GET /sets/search
# -------------------------


def test_search_sets(client):
    with patch("app.controller.search_controller.SearchService") as mock_svc:
        mock_svc.return_value.search_sets.return_value = [{"set_num": "1234-1"}]

        resp = client.get("/sets/search?q=castle")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_search_sets_with_filters(client):
    with patch("app.controller.search_controller.SearchService") as mock_svc:
        mock_svc.return_value.search_sets.return_value = []

        resp = client.get("/sets/search?q=castle&theme_id=1&year_from=2020&year_to=2023&limit=5")

    assert resp.status_code == 200
    mock_svc.return_value.search_sets.assert_called_once_with("castle", 1, 2020, 2023, 5)


# -------------------------
# GET /parts/search
# -------------------------


def test_search_parts(client):
    with patch("app.controller.search_controller.SearchService") as mock_svc:
        mock_svc.return_value.search_parts.return_value = [{"part_num": "3001"}]

        resp = client.get("/parts/search?q=brick")

    assert resp.status_code == 200


# -------------------------
# GET /sets/recent
# -------------------------


def test_get_recent_sets(client):
    with patch("app.controller.search_controller.SearchService") as mock_svc:
        mock_svc.return_value.get_recent_sets.return_value = [{"set_num": "1234-1"}]

        resp = client.get("/sets/recent")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


# -------------------------
# GET /stats
# -------------------------


def test_get_stats(client):
    with patch("app.controller.search_controller.SearchService") as mock_svc:
        mock_svc.return_value.get_stats.return_value = {"total_sets": 1000}

        resp = client.get("/stats")

    assert resp.status_code == 200
    assert resp.json()["total_sets"] == 1000
