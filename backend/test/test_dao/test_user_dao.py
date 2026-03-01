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
