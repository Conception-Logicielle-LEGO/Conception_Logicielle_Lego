from app.business_object.buildable_set import BuildableSet


def make_buildable_set(completion=100.0, missing_parts_count=0):
    return BuildableSet(
        set_num="1234-1",
        name="Castle",
        year=2000,
        theme_id=1,
        num_parts=50,
        total_parts_needed=10,
        parts_owned=int(10 * completion / 100),
        completion_percentage=completion,
        missing_parts_count=missing_parts_count,
    )


def test_is_buildable_true():
    assert make_buildable_set(completion=100.0).is_buildable() is True


def test_is_buildable_false():
    assert make_buildable_set(completion=90.0).is_buildable() is False


def test_is_almost_buildable_above_threshold():
    assert make_buildable_set(completion=85.0).is_almost_buildable(threshold=80.0) is True


def test_is_almost_buildable_below_threshold():
    assert make_buildable_set(completion=70.0).is_almost_buildable(threshold=80.0) is False


def test_get_priority_score_buildable():
    assert make_buildable_set(completion=100.0).get_priority_score() == 100.0


def test_get_priority_score_partial():
    s = make_buildable_set(completion=90.0, missing_parts_count=5)
    score = s.get_priority_score()
    assert score < 90.0
    assert score > 0


def test_get_priority_score_penalty_capped():
    # missing_parts_count > 100 → penalty plafonné à 0.5
    s = make_buildable_set(completion=80.0, missing_parts_count=200)
    assert s.get_priority_score() == 80.0 * (1 - 0.5)


def test_from_dict():
    data = {
        "set_num": "1234-1", "name": "Castle", "year": 2000,
        "theme_id": 1, "num_parts": 50,
        "total_parts_needed": 10, "parts_owned": 10,
        "completion_percentage": 100.0, "missing_parts_count": 0,
    }
    s = BuildableSet.from_dict(data)
    assert s.set_num == "1234-1"
    assert s.img_url is None
    assert s.missing_parts is None


def test_to_dict_basic():
    s = make_buildable_set(completion=100.0)
    d = s.to_dict()
    assert "set" in d
    assert "buildability" in d
    assert d["buildability"]["is_buildable"] is True
    assert "missing_parts" not in d


def test_to_dict_with_missing_parts():
    s = make_buildable_set(completion=90.0)
    s.missing_parts = [{"part_num": "3001"}]
    d = s.to_dict()
    assert "missing_parts" in d


def test_str_buildable():
    s = make_buildable_set(completion=100.0)
    assert "✅" in str(s)
    assert "100%" in str(s)


def test_str_not_buildable():
    s = make_buildable_set(completion=85.0)
    assert "🔨" in str(s)
    assert "85%" in str(s)
