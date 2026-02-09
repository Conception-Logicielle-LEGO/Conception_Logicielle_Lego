from app.database.connexion import get_table_count


def test_create_update_delete_user_ok(user_dao):  # clean_user_tables en argument ?
    """Test avec nettoyage des tables utilisateur"""
    res1 = get_table_count(table_name="users", test=True)  # avant insertion
    # insertion user
    user = user_dao.create_user("testuser", "password123")
    assert user is not None
    assert user.username == "testuser"

    res2 = get_table_count(table_name="users", test=True)  # après insertion
    assert res2 == res1 + 1

    # Update username
    update_username_status = user_dao.update_user(
        update_username=True, new_entry="MartinLeGalopin", id_user=user.id_user
    )
    assert update_username_status is True
    res3 = get_table_count(table_name="users", test=True)  # après update username

    # Update password
    update_password_status = user_dao.update_user(
        update_username=True, new_entry="top_top_secret", id_user=user.id_user
    )
    assert update_password_status is True
    res4 = get_table_count(table_name="users", test=True)  # après update password
    assert res2 == res3 == res4

    # delete user
    deleted_status = user_dao.delete_user(user.id_user)
    assert deleted_status is True
    res5 = get_table_count(table_name="users", test=True)  # après delete password
    assert res5 == res4 - 1
