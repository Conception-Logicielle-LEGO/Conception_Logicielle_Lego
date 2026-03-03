from app.business_object.theme import Theme


def test_theme_init_root():
    t = Theme(id=158, name="Star Wars")
    assert t.id == 158
    assert t.name == "Star Wars"
    assert t.parent_id is None


def test_theme_init_sub():
    t = Theme(id=200, name="Episode IV", parent_id=158)
    assert t.parent_id == 158


def test_theme_str_root():
    t = Theme(id=158, name="Star Wars")
    assert str(t) == "Theme Star Wars"


def test_theme_str_sub():
    t = Theme(id=200, name="Episode IV", parent_id=158)
    assert str(t) == "Theme Episode IV (parent=158)"


def test_theme_repr():
    t = Theme(id=158, name="Star Wars")
    assert repr(t) == "Theme(id=158, name='Star Wars')"


def test_theme_from_dict():
    data = {"id": 158, "name": "Star Wars", "parent_id": None}
    t = Theme.from_dict(data)
    assert t.id == 158
    assert t.parent_id is None


def test_theme_to_dict():
    t = Theme(id=158, name="Star Wars", parent_id=None)
    assert t.to_dict() == {"id": 158, "name": "Star Wars", "parent_id": None}


def test_theme_is_sub_theme():
    assert Theme(id=200, name="Episode IV", parent_id=158).is_sub_theme() is True
    assert Theme(id=158, name="Star Wars").is_sub_theme() is False


def test_theme_is_root_theme():
    assert Theme(id=158, name="Star Wars").is_root_theme() is True
    assert Theme(id=200, name="Episode IV", parent_id=158).is_root_theme() is False
