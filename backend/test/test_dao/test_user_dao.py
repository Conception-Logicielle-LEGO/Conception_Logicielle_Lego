"""
Tests d'intégration pour les opérations CRUD sur la table users (PostgreSQL).

Lancement :
    pytest test/test_dao/test_user_dao.py -v
"""


class TestCreateUser:
    def test_create_user_inserted_in_db(self, pg_conn):
        with pg_conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as count FROM users")
            count_before = cur.fetchone()["count"]

            cur.execute(
                "INSERT INTO users (username, hashed_password, email) VALUES (%s, %s, %s)",
                ("nouveau_user", "hashed_pw", "nouveau@test.com"),
            )

            cur.execute("SELECT COUNT(*) as count FROM users")
            assert cur.fetchone()["count"] == count_before + 1

    def test_create_user_fields_persisted(self, pg_conn):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password, email) VALUES (%s, %s, %s) RETURNING id_user",
                ("alice", "hashed_pw", "alice@test.com"),
            )
            user_id = cur.fetchone()["id_user"]

            cur.execute("SELECT * FROM users WHERE id_user = %s", (user_id,))
            row = cur.fetchone()

        assert row["username"] == "alice"
        assert row["email"] == "alice@test.com"

    def test_duplicate_username_raises(self, pg_conn):
        import psycopg2

        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                ("bob", "pw"),
            )
        pg_conn.commit()

        with pg_conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                    ("bob", "pw2"),
                )
                pg_conn.commit()
                raise AssertionError("Aurait dû lever une erreur d'unicité")
            except psycopg2.errors.UniqueViolation:
                pg_conn.rollback()


class TestUpdateUser:
    def test_update_username(self, pg_conn, existing_user):
        with pg_conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET username = %s WHERE id_user = %s RETURNING id_user",
                ("nouveau_nom", existing_user),
            )
            assert cur.fetchone() is not None

            cur.execute(
                "SELECT username FROM users WHERE id_user = %s", (existing_user,)
            )
            assert cur.fetchone()["username"] == "nouveau_nom"


class TestDeleteUser:
    def test_delete_user_removed_from_db(self, pg_conn, existing_user):
        with pg_conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id_user = %s", (existing_user,))

            cur.execute(
                "SELECT id_user FROM users WHERE id_user = %s", (existing_user,)
            )
            assert cur.fetchone() is None

    def test_delete_nonexistent_user_affects_zero_rows(self, pg_conn):
        with pg_conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id_user = %s", (-999,))
            assert cur.rowcount == 0


class TestUserDAO:
    """Tests utilisant la classe UserDAO directement."""

    def test_create_user_via_dao(self, pg_conn):
        from app.business_object.user import User
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        user = User(username="dao_user", hashed_password="hash", salt="salt")
        result = dao.create_user(user)

        assert result is not None
        assert result.username == "dao_user"
        assert result.id_user is not None

    def test_create_user_duplicate_returns_none(self, pg_conn):
        from app.business_object.user import User
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        user = User(username="dup_user", hashed_password="hash", salt="salt")
        dao.create_user(user)
        pg_conn.commit()
        result = dao.create_user(user)
        pg_conn.rollback()

        assert result is None

    def test_get_by_username_found(self, pg_conn, existing_user):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.get_by_username("test_user")

        assert result is not None
        assert result.username == "test_user"

    def test_get_by_username_not_found(self, pg_conn):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.get_by_username("inconnu")

        assert result is None

    def test_get_by_id_found(self, pg_conn, existing_user):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.get_by_id(existing_user)

        assert result is not None
        assert result.id_user == existing_user

    def test_get_by_id_not_found(self, pg_conn):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.get_by_id(-999)

        assert result is None

    def test_is_username_taken_true(self, pg_conn, existing_user):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        assert dao.is_username_taken("test_user") is True

    def test_is_username_taken_false(self, pg_conn):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        assert dao.is_username_taken("utilisateur_inexistant") is False

    def test_update_user_username(self, pg_conn, existing_user):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.update_user(True, "nouveau_nom", existing_user)

        assert result is True
        updated = dao.get_by_id(existing_user)
        assert updated.username == "nouveau_nom"

    def test_update_user_password(self, pg_conn, existing_user):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.update_user(False, "new_hashed_pw", existing_user)

        assert result is True

    def test_update_user_not_found(self, pg_conn):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.update_user(True, "nom", -999)

        assert result is False

    def test_delete_user_via_dao(self, pg_conn, existing_user):
        from app.database.dao.user_dao import UserDAO

        dao = UserDAO(pg_conn)
        result = dao.delete_user(existing_user)

        assert result is True
        assert dao.get_by_id(existing_user) is None


# ---------------------------------------------------------------------------
# Tests avec mock — chemins d'exception (sans PostgreSQL)
# ---------------------------------------------------------------------------


class TestUserDAOMockPaths:
    def test_create_user_fetchone_returns_none(self):
        """Couvre le chemin row is None dans create_user."""
        from unittest.mock import MagicMock
        from app.database.dao.user_dao import UserDAO
        from app.business_object.user import User

        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None

        dao = UserDAO(mock_conn)
        user = User(username="x", hashed_password="h", salt="s")
        result = dao.create_user(user)

        assert result is None

    def test_delete_user_exception_returns_false(self):
        """Couvre le chemin except dans delete_user."""
        from unittest.mock import MagicMock
        from app.database.dao.user_dao import UserDAO

        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.execute.side_effect = Exception("DB error")

        dao = UserDAO(mock_conn)
        result = dao.delete_user(99)

        assert result is False
