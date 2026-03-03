from datetime import datetime
from app.business_object.favorite_set import FavoriteSet


def test_favorite_set_init():
    fs = FavoriteSet(id_user=1, set_num="1234-1")
    assert fs.id_user == 1
    assert fs.set_num == "1234-1"
    assert fs.added_at is None


def test_favorite_set_str():
    fs = FavoriteSet(id_user=1, set_num="1234-1")
    assert str(fs) == "FavoriteSet 1234-1 (user=1)"


def test_favorite_set_repr():
    fs = FavoriteSet(id_user=1, set_num="1234-1")
    assert "1234-1" in repr(fs)


def test_favorite_set_eq_same():
    fs1 = FavoriteSet(id_user=1, set_num="1234-1")
    fs2 = FavoriteSet(id_user=1, set_num="1234-1")
    assert fs1 == fs2


def test_favorite_set_eq_different_set():
    fs1 = FavoriteSet(id_user=1, set_num="1234-1")
    fs2 = FavoriteSet(id_user=1, set_num="9999-1")
    assert fs1 != fs2


def test_favorite_set_eq_different_user():
    fs1 = FavoriteSet(id_user=1, set_num="1234-1")
    fs2 = FavoriteSet(id_user=2, set_num="1234-1")
    assert fs1 != fs2


def test_favorite_set_eq_different_type():
    fs = FavoriteSet(id_user=1, set_num="1234-1")
    assert fs != "not a FavoriteSet"


def test_favorite_set_from_dict():
    data = {"id_user": 1, "set_num": "1234-1", "added_at": None}
    fs = FavoriteSet.from_dict(data)
    assert fs.id_user == 1


def test_favorite_set_to_dict_no_date():
    fs = FavoriteSet(id_user=1, set_num="1234-1")
    d = fs.to_dict()
    assert d["added_at"] is None


def test_favorite_set_to_dict_with_date():
    dt = datetime(2024, 6, 1)
    fs = FavoriteSet(id_user=1, set_num="1234-1", added_at=dt)
    d = fs.to_dict()
    assert d["added_at"] == dt.isoformat()
