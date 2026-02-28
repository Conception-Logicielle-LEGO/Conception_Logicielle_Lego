from backend.app.business_object.part import Part

from app.database.connexion_duckdb import (
    execute_duckdb_query,
)


class PartsDAO:
    def __init__(self, duckdb_connection):
        self.conn = duckdb_connection()

    def get_by(self, column: str, value) -> list[dict]:
        # Liste blanche pour éviter les injections SQL via le nom de colonne
        allowed_columns = {"id_user", "part_num", "status_owned_wished", "is_used"}

        if column not in allowed_columns:
            raise ValueError(f"Colonne '{column}' non autorisée.")

        query = f"""
            SELECT *
            FROM user_parts
            WHERE {column} = %(value)s;
         """
        rows = execute_duckdb_query(query=query, params={"value": value})

        # Chaque ligne est convertie avec from_dict
        return [Part.from_dict(row) for row in rows]
