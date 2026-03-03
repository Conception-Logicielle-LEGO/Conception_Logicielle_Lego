from app.business_object.set import Set


def test_set_init():
    s = Set(
        set_num="75192-1",
        name="Millennium Falcon",
        year=2017,
        theme_id=158,
        num_parts=7541,
    )
    assert s.set_num == "75192-1"
    assert s.name == "Millennium Falcon"
    assert s.year == 2017
    assert s.theme_id == 158
    assert s.num_parts == 7541
    assert s.img_url is None


def test_set_init_with_img():
    s = Set(
        set_num="75192-1",
        name="Falcon",
        year=2017,
        theme_id=158,
        num_parts=100,
        img_url="http://img",
    )
    assert s.img_url == "http://img"


def test_set_str():
    s = Set(
        set_num="75192-1",
        name="Millennium Falcon",
        year=2017,
        theme_id=158,
        num_parts=7541,
    )
    assert str(s) == "Set 75192-1: Millennium Falcon (2017) - 7541 pièces"


def test_set_repr():
    s = Set(
        set_num="75192-1",
        name="Millennium Falcon",
        year=2017,
        theme_id=158,
        num_parts=7541,
    )
    assert repr(s) == "Set(set_num='75192-1', name='Millennium Falcon')"


def test_set_from_dict():
    data = {
        "set_num": "1234-1",
        "name": "Castle",
        "year": 2000,
        "theme_id": 1,
        "num_parts": 500,
    }
    s = Set.from_dict(data)
    assert s.set_num == "1234-1"
    assert s.name == "Castle"
    assert s.img_url is None


def test_set_to_dict():
    s = Set(
        set_num="1234-1",
        name="Castle",
        year=2000,
        theme_id=1,
        num_parts=500,
        img_url="http://img",
    )
    d = s.to_dict()
    assert d == {
        "set_num": "1234-1",
        "name": "Castle",
        "year": 2000,
        "theme_id": 1,
        "num_parts": 500,
        "img_url": "http://img",
    }
