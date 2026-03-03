from datetime import datetime

from app.business_object.wishlist_set import WishlistSet


def test_wishlist_set_init():
    ws = WishlistSet(id_wishlist=1, set_num="1234-1")
    assert ws.id_wishlist == 1
    assert ws.set_num == "1234-1"
    assert ws.priority == 0
    assert ws.added_at is None


def test_wishlist_set_str():
    ws = WishlistSet(id_wishlist=1, set_num="1234-1", priority=3)
    assert str(ws) == "WishlistSet 1234-1 (priority=3)"


def test_wishlist_set_repr():
    ws = WishlistSet(id_wishlist=1, set_num="1234-1", priority=2)
    assert repr(ws) == "WishlistSet(id_wishlist=1, set_num='1234-1', priority=2)"


def test_wishlist_set_from_dict():
    data = {"id_wishlist": 1, "set_num": "1234-1", "priority": 5}
    ws = WishlistSet.from_dict(data)
    assert ws.priority == 5
    assert ws.added_at is None


def test_wishlist_set_to_dict_no_date():
    ws = WishlistSet(id_wishlist=1, set_num="1234-1", priority=0)
    d = ws.to_dict()
    assert d["added_at"] is None


def test_wishlist_set_to_dict_with_date():
    dt = datetime(2024, 1, 15)
    ws = WishlistSet(id_wishlist=1, set_num="1234-1", added_at=dt)
    d = ws.to_dict()
    assert d["added_at"] == dt.isoformat()


def test_increase_priority():
    ws = WishlistSet(id_wishlist=1, set_num="1234-1", priority=2)
    ws.increase_priority()
    assert ws.priority == 3


def test_decrease_priority():
    ws = WishlistSet(id_wishlist=1, set_num="1234-1", priority=2)
    ws.decrease_priority()
    assert ws.priority == 1


def test_decrease_priority_min_zero():
    ws = WishlistSet(id_wishlist=1, set_num="1234-1", priority=0)
    ws.decrease_priority()
    assert ws.priority == 0
