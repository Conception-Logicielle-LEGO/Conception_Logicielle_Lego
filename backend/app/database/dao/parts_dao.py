class OwnedPartsDAO:
    def __init__(self, db_connection):
        self.conn = db_connection(read_only=False)

    def get_by(self, column: str, value) -> list[dict]:
        # Liste blanche pour éviter les injections SQL via le nom de colonne
        allowed_columns = {
            "id_user",
            "part_num",
            "status_owned_wished",
            "is_used"
            }

        if column not in allowed_columns:
            raise ValueError(f"Colonne '{column}' non autorisée.")

        query = f"""
            SELECT *
            FROM user_parts
            WHERE {column} = %(value)s;
        """

        with db_connection().connection.cursor() as cursor:
            cursor.execute(query, {"value": value})
            rows = cursor.fetchall()

        # Chaque ligne est convertie avec ton from_dict
        return [Owned_part.from_dict(row) for row in rows]