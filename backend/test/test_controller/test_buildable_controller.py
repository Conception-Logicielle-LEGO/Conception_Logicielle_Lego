from unittest.mock import MagicMock, patch


def test_get_buildable_sets(client):
    mock_set = MagicMock()
    mock_set.to_dict.return_value = {"set_num": "1234-1", "completion_percentage": 100.0}

    with patch("app.controller.buildable_controller.BuildableService") as mock_svc:
        mock_svc.return_value.get_buildable_sets.return_value = {
            "buildable": [mock_set],
            "partial": [],
        }

        resp = client.get("/users/1/buildable")

    assert resp.status_code == 200
    result = resp.json()
    assert "buildable" in result
    assert "partial" in result
    assert len(result["buildable"]) == 1


def test_get_buildable_sets_empty(client):
    with patch("app.controller.buildable_controller.BuildableService") as mock_svc:
        mock_svc.return_value.get_buildable_sets.return_value = {
            "buildable": [],
            "partial": [],
        }

        resp = client.get("/users/1/buildable")

    assert resp.status_code == 200
    assert resp.json() == {"buildable": [], "partial": []}


def test_get_buildable_sets_with_limit(client):
    with patch("app.controller.buildable_controller.BuildableService") as mock_svc:
        mock_svc.return_value.get_buildable_sets.return_value = {
            "buildable": [],
            "partial": [],
        }

        client.get("/users/1/buildable?limit=10")

        mock_svc.return_value.get_buildable_sets.assert_called_once_with(1, 10)
