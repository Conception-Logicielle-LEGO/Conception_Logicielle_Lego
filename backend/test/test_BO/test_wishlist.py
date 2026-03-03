from datetime import datetime

from app.business_object.wishlist import Wishlist


def test_wishlist_init():
    w = Wishlist(id_user=1)
    assert w.id_user == 1
    assert w.id_wishlist is None
    assert w.created_at is None


def test_wishlist_str():
    w = Wishlist(id_user=1, id_wishlist=10)
    assert str(w) == "Wishlist(id=10, user=1)"


def test_wishlist_from_dict():
    data = {"id_wishlist": 5, "id_user": 3, "created_at": None}
    w = Wishlist.from_dict(data)
    assert w.id_wishlist == 5
    assert w.id_user == 3


def test_wishlist_to_dict():
    dt = datetime(2024, 1, 1)
    w = Wishlist(id_user=1, id_wishlist=5, created_at=dt)
    d = w.to_dict()
    assert d == {"id_wishlist": 5, "id_user": 1, "created_at": dt}
