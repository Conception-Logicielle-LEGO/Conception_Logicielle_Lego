from app.business_object.user import User


def test_user_init():
    user = User(username="john", hashed_password="hash", salt="salt")
    assert user.username == "john"
    assert user.hashed_password == "hash"
    assert user.salt == "salt"
    assert user.id_user is None


def test_user_init_with_id():
    user = User(username="john", hashed_password="hash", salt="salt", id_user=42)
    assert user.id_user == 42


def test_user_str():
    user = User(username="john", hashed_password="hash", salt="salt", id_user=1)
    assert str(user) == "john (id=1)"


def test_user_from_dict():
    data = {"id_user": 5, "username": "alice", "hashed_password": "h", "salt": "s"}
    user = User.from_dict(data)
    assert user.id_user == 5
    assert user.username == "alice"
    assert user.hashed_password == "h"
    assert user.salt == "s"


def test_user_from_dict_missing_id():
    data = {"username": "alice", "hashed_password": "h", "salt": "s"}
    user = User.from_dict(data)
    assert user.id_user is None


def test_user_to_dict():
    user = User(username="john", hashed_password="hash", salt="salt", id_user=1)
    d = user.to_dict()
    assert d == {
        "id_user": 1,
        "username": "john",
        "hashed_password": "hash",
        "salt": "salt",
    }
