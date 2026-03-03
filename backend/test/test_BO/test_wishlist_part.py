from datetime import datetime

from app.business_object.wishlist_part import WishlistPart


def test_wishlist_part_init():
    wp = WishlistPart(id_wishlist=1, part_num="3001", color_id=4)
    assert wp.id_wishlist == 1
    assert wp.part_num == "3001"
    assert wp.color_id == 4
    assert wp.quantity == 1
    assert wp.added_at is None


def test_wishlist_part_str():
    wp = WishlistPart(id_wishlist=1, part_num="3001", color_id=4, quantity=3)
    assert str(wp) == "WishlistPart 3001 (color=4, qty=3)"


def test_wishlist_part_repr():
    wp = WishlistPart(id_wishlist=1, part_num="3001", color_id=4)
    assert repr(wp) == "WishlistPart(id_wishlist=1, part_num='3001', color_id=4)"


def test_wishlist_part_from_dict():
    data = {"id_wishlist": 1, "part_num": "3001", "color_id": 4, "quantity": 2}
    wp = WishlistPart.from_dict(data)
    assert wp.quantity == 2
    assert wp.added_at is None


def test_wishlist_part_to_dict_no_date():
    wp = WishlistPart(id_wishlist=1, part_num="3001", color_id=4)
    d = wp.to_dict()
    assert d["added_at"] is None
    assert d["quantity"] == 1


def test_wishlist_part_to_dict_with_date():
    dt = datetime(2024, 3, 10)
    wp = WishlistPart(id_wishlist=1, part_num="3001", color_id=4, added_at=dt)
    d = wp.to_dict()
    assert d["added_at"] == dt.isoformat()
