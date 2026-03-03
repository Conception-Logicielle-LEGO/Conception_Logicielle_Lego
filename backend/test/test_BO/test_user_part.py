from app.business_object.user_part import UserPart


def test_user_part_init():
    up = UserPart(id_user=1, part_num="3001", color_id=4)
    assert up.quantity == 1
    assert up.status == "owned"
    assert up.is_used is False
    assert up.added_at is None


def test_user_part_str():
    up = UserPart(
        id_user=1,
        part_num="3001",
        color_id=4,
        quantity=3,
        status="owned",
        is_used=False,
    )
    assert "3001" in str(up)
    assert "owned" in str(up)


def test_user_part_repr():
    up = UserPart(id_user=1, part_num="3001", color_id=4, status="wished")
    assert "wished" in repr(up)


def test_user_part_from_dict():
    data = {
        "id_user": 1,
        "part_num": "3001",
        "color_id": 4,
        "quantity": 2,
        "status": "owned",
    }
    up = UserPart.from_dict(data)
    assert up.quantity == 2
    assert up.is_used is False


def test_user_part_to_dict():
    up = UserPart(id_user=1, part_num="3001", color_id=4, quantity=2, status="owned")
    d = up.to_dict()
    assert d["part_num"] == "3001"
    assert d["added_at"] is None


def test_is_owned():
    assert (
        UserPart(id_user=1, part_num="3001", color_id=4, status="owned").is_owned()
        is True
    )
    assert (
        UserPart(id_user=1, part_num="3001", color_id=4, status="wished").is_owned()
        is False
    )


def test_is_wished():
    assert (
        UserPart(id_user=1, part_num="3001", color_id=4, status="wished").is_wished()
        is True
    )
    assert (
        UserPart(id_user=1, part_num="3001", color_id=4, status="owned").is_wished()
        is False
    )


def test_mark_as_used():
    up = UserPart(id_user=1, part_num="3001", color_id=4)
    up.mark_as_used()
    assert up.is_used is True


def test_mark_as_free():
    up = UserPart(id_user=1, part_num="3001", color_id=4, is_used=True)
    up.mark_as_free()
    assert up.is_used is False


def test_add_quantity():
    up = UserPart(id_user=1, part_num="3001", color_id=4, quantity=3)
    up.add_quantity(5)
    assert up.quantity == 8


def test_remove_quantity():
    up = UserPart(id_user=1, part_num="3001", color_id=4, quantity=5)
    up.remove_quantity(3)
    assert up.quantity == 2


def test_remove_quantity_min_zero():
    up = UserPart(id_user=1, part_num="3001", color_id=4, quantity=2)
    up.remove_quantity(10)
    assert up.quantity == 0
