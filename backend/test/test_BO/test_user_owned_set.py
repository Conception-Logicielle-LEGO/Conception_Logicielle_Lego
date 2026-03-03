from app.business_object.user_owned_set import UserOwnedSet


def test_user_owned_set_init():
    s = UserOwnedSet(id_user=1, set_num="1234-1")
    assert s.id_user == 1
    assert s.set_num == "1234-1"
    assert s.is_built is False


def test_user_owned_set_str_unbuilt():
    s = UserOwnedSet(id_user=1, set_num="1234-1", is_built=False)
    assert str(s) == "UserOwnedSet 1234-1 (user=1, non construit)"


def test_user_owned_set_str_built():
    s = UserOwnedSet(id_user=1, set_num="1234-1", is_built=True)
    assert str(s) == "UserOwnedSet 1234-1 (user=1, construit)"


def test_user_owned_set_repr():
    s = UserOwnedSet(id_user=1, set_num="1234-1", is_built=False)
    assert repr(s) == "UserOwnedSet(id_user=1, set_num='1234-1', is_built=False)"


def test_user_owned_set_from_dict():
    data = {"id_user": 2, "set_num": "5678-1", "is_built": True}
    s = UserOwnedSet.from_dict(data)
    assert s.is_built is True


def test_user_owned_set_from_dict_default_is_built():
    data = {"id_user": 2, "set_num": "5678-1"}
    s = UserOwnedSet.from_dict(data)
    assert s.is_built is False


def test_user_owned_set_to_dict():
    s = UserOwnedSet(id_user=1, set_num="1234-1", is_built=True)
    assert s.to_dict() == {"id_user": 1, "set_num": "1234-1", "is_built": True}


def test_mark_as_built():
    s = UserOwnedSet(id_user=1, set_num="1234-1", is_built=False)
    s.mark_as_built()
    assert s.is_built is True


def test_mark_as_unbuilt():
    s = UserOwnedSet(id_user=1, set_num="1234-1", is_built=True)
    s.mark_as_unbuilt()
    assert s.is_built is False
