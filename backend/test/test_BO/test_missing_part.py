from app.business_object.missing_part import MissingPart


def test_missing_part_init():
    mp = MissingPart(part_num="3001", color_id=4, needed=5, owned=2, missing=3)
    assert mp.part_num == "3001"
    assert mp.missing == 3
    assert mp.part_name is None


def test_is_completely_missing():
    mp = MissingPart(part_num="3001", color_id=4, needed=5, owned=0, missing=5)
    assert mp.is_completely_missing() is True


def test_is_not_completely_missing():
    mp = MissingPart(part_num="3001", color_id=4, needed=5, owned=2, missing=3)
    assert mp.is_completely_missing() is False


def test_get_completion_percentage():
    mp = MissingPart(part_num="3001", color_id=4, needed=10, owned=7, missing=3)
    assert mp.get_completion_percentage() == 70.0


def test_get_completion_percentage_zero_needed():
    mp = MissingPart(part_num="3001", color_id=4, needed=0, owned=0, missing=0)
    assert mp.get_completion_percentage() == 100.0


def test_from_dict():
    data = {"part_num": "3001", "color_id": 4, "needed": 5, "missing": 3}
    mp = MissingPart.from_dict(data)
    assert mp.owned == 0
    assert mp.part_name is None


def test_to_dict_basic():
    mp = MissingPart(part_num="3001", color_id=4, needed=5, owned=2, missing=3)
    d = mp.to_dict()
    assert d["part_num"] == "3001"
    assert d["quantity"] == {"needed": 5, "owned": 2, "missing": 3}
    assert "details" not in d


def test_to_dict_with_details():
    mp = MissingPart(part_num="3001", color_id=4, needed=5, owned=2, missing=3,
                     part_name="Brick", color_name="Red", color_rgb="FF0000")
    d = mp.to_dict()
    assert "details" in d
    assert d["details"]["part_name"] == "Brick"
    assert d["details"]["color_rgb"] == "#FF0000"


def test_str_with_part_name_and_color():
    mp = MissingPart(part_num="3001", color_id=4, needed=5, owned=2, missing=3,
                     part_name="Brick", color_name="Red")
    assert "Brick" in str(mp)
    assert "Red" in str(mp)
    assert "3" in str(mp)


def test_str_without_part_name():
    mp = MissingPart(part_num="3001", color_id=4, needed=5, owned=0, missing=5)
    assert "3001" in str(mp)
