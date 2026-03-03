from app.business_object.color import Color


def test_color_init():
    c = Color(id=0, name="Black", rgb="05131D")
    assert c.id == 0
    assert c.name == "Black"
    assert c.rgb == "05131D"
    assert c.is_trans is False


def test_color_str_opaque():
    c = Color(id=0, name="Black", rgb="05131D")
    assert str(c) == "Color Black #05131D"


def test_color_str_transparent():
    c = Color(id=1, name="Trans-Clear", rgb="FFFFFF", is_trans=True)
    assert str(c) == "Color Trans-Clear #FFFFFF (transparent)"


def test_color_repr():
    c = Color(id=0, name="Black", rgb="05131D")
    assert repr(c) == "Color(id=0, name='Black', rgb='05131D')"


def test_color_from_dict():
    data = {"id": 4, "name": "Red", "rgb": "C91A09", "is_trans": False}
    c = Color.from_dict(data)
    assert c.id == 4
    assert c.name == "Red"
    assert c.is_trans is False


def test_color_from_dict_defaults_is_trans():
    data = {"id": 4, "name": "Red", "rgb": "C91A09"}
    c = Color.from_dict(data)
    assert c.is_trans is False


def test_color_to_dict():
    c = Color(id=0, name="Black", rgb="05131D", is_trans=False)
    assert c.to_dict() == {"id": 0, "name": "Black", "rgb": "05131D", "is_trans": False}


def test_color_get_hex_color():
    c = Color(id=0, name="Black", rgb="05131D")
    assert c.get_hex_color() == "#05131D"
