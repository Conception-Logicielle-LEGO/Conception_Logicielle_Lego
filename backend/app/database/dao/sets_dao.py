# from app.database.connexion import db_connection


class OwnedSetsDAO:
    def __init__(self, db_connection):
        self.conn = db_connection(read_only=False)

    def get_by(self, column: str, value) -> list[dict]:
        ## Liste blanche pour éviter les injections SQL via le nom de colonne
        # allowed_columns = {"id_user", "set_num"}
        #
        # if column not in allowed_columns:
        #    raise ValueError(f"Colonne '{column}' non autorisée.")
        #
        # query = f"""
        #    SELECT *
        #    FROM owned_sets
        #    WHERE {column} = %(value)s;
        # """
        #
        # with db_connection().connection.cursor() as cursor:
        #    cursor.execute(query, {"value": value})
        #    rows = cursor.fetchall()
        #
        ## Chaque ligne est convertie avec ton from_dict
        # return [Owned_set.from_dict(row) for row in rows]
        pass
