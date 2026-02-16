from app.business_object.set import Set
from app.business_object.user_owned_set import UserOwnedSet, UserSetWithDetails
from app.database.dao.base_dao import BaseDAO


class SetDAO(BaseDAO):
    """
    DAO pour gérer les sets LEGO dans la base de données.
    Gère à la fois le catalogue Rebrickable (table sets)
    et les sets possédés par les utilisateurs (table user_owned_sets).
    """

    def get_table_name(self) -> str:
        """Table principale : user_owned_sets"""
        return "user_owned_sets"

    def get_allowed_columns(self) -> set[str]:
        """Colonnes autorisées pour les requêtes get_by()"""
        return {"id_user", "set_num", "is_built"}

    # def from_row(self, row: dict) -> Set:
    #    """
    #    Convertit une ligne SQL en dictionnaire.
    #    Pour user_owned_sets, on retourne un dict car on n'a pas de BO dédié.
    #    """
    #    return row

    def get_user_sets(self, id_user: int) -> list[dict]:
        """
        Récupère tous les sets possédés par un utilisateur avec leurs détails.

        Paramètre :
        -----------
        id_user : int
            ID de l'utilisateur

        Renvoie :
        ---------
        list[dict] :
            Liste de dictionnaires contenant :
            - set_num : Numéro du set (ex: "75192-1")
            - name : Nom du set
            - year : Année de sortie
            - theme_id : ID du thème
            - num_parts : Nombre de pièces
            - is_built : Statut de construction (True/False)
        """
        query = """
            SELECT
                uos.set_num,
                s.name,
                s.year,
                s.theme_id,
                s.num_parts,
                uos.is_built
            FROM user_owned_sets uos
            JOIN sets s ON uos.set_num = s.set_num
            WHERE uos.id_user = ?
            ORDER BY s.name;
        """
        result = self.conn.execute(query, [id_user]).fetchall()
        return [dict(row) for row in result]

    def add_owned_set(self, id_user: int, set_num: str, is_built: bool = False) -> bool:
        """
        Ajoute un set à la collection d'un utilisateur.

        Paramètres :
        ------------
        id_user : int
            ID de l'utilisateur
        set_num : str
            Numéro du set (ex: "75192-1")
        is_built : bool, optional
            Statut de construction (défaut : False)

        Renvoie :
        ---------
        bool :
            True si succès, False si échec (set déjà possédé ou inexistant)
        """
        try:
            # Vérifier que le set existe dans le catalogue
            if not self.set_exists_in_catalog(set_num):
                print(f"Error: Set {set_num} not found in catalog")
                return False

            self.conn.execute(
                """
                INSERT INTO user_owned_sets (id_user, set_num, is_built)
                VALUES (?, ?, ?)
                """,
                [id_user, set_num, is_built],
            )
            return True
        except Exception as e:
            print(f"Error adding owned set: {e}")
            return False

    def remove_owned_set(self, id_user: int, set_num: str) -> bool:
        """
        Retire un set de la collection d'un utilisateur.

        Paramètres :
        ------------
        id_user : int
            ID de l'utilisateur
        set_num : str
            Numéro du set à retirer

        Renvoie :
        ---------
        bool :
            True si succès, False si échec
        """
        try:
            result = self.conn.execute(
                """
                DELETE FROM user_owned_sets
                WHERE id_user = ? AND set_num = ?
                RETURNING set_num;
                """,
                [id_user, set_num],
            ).fetchone()
            return result is not None
        except Exception as e:
            print(f"Error removing owned set: {e}")
            return False

    def mark_as_built(self, id_user: int, set_num: str, is_built: bool = True) -> bool:
        """
        Marque un set comme construit ou non construit.

        Paramètres :
        ------------
        id_user : int
            ID de l'utilisateur
        set_num : str
            Numéro du set
        is_built : bool, optional
            Statut de construction (défaut : True)

        Renvoie :
        ---------
        bool :
            True si succès, False si échec
        """
        try:
            result = self.conn.execute(
                """
                UPDATE user_owned_sets
                SET is_built = ?
                WHERE id_user = ? AND set_num = ?
                RETURNING set_num;
                """,
                [is_built, id_user, set_num],
            ).fetchone()
            return result is not None
        except Exception as e:
            print(f"Error marking set as built: {e}")
            return False

    def set_exists_in_catalog(self, set_num: str) -> bool:
        """
        Vérifie si un set existe dans le catalogue Rebrickable.

        Paramètre :
        -----------
        set_num : str
            Numéro du set à vérifier

        Renvoie :
        ---------
        bool :
            True si le set existe, False sinon
        """
        query = "SELECT COUNT(*) as count FROM sets WHERE set_num = ?;"
        result = self.conn.execute(query, [set_num]).fetchone()
        return result["count"] > 0 if result else False

    def get_set_details(self, set_num: str) -> dict | None:
        """
        Récupère les détails d'un set depuis le catalogue Rebrickable.

        Paramètre :
        -----------
        set_num : str
            Numéro du set

        Renvoie :
        ---------
        dict | None :
            Dictionnaire avec les détails du set ou None si inexistant
        """
        query = """
            SELECT set_num, name, year, theme_id, num_parts
            FROM sets
            WHERE set_num = ?;
        """
        result = self.conn.execute(query, [set_num]).fetchone()
        return dict(result) if result else None

    def get_set_parts(self, set_num: str) -> list[dict]:
        """
        Récupère toutes les pièces nécessaires pour construire un set.

        Paramètre :
        -----------
        set_num : str
            Numéro du set

        Renvoie :
        ---------
        list[dict] :
            Liste de dictionnaires contenant :
            - part_num : Numéro de la pièce
            - color_id : ID de la couleur
            - quantity : Quantité nécessaire
            - part_name : Nom de la pièce
            - color_name : Nom de la couleur
        """
        query = """
            SELECT
                ip.part_num,
                ip.color_id,
                ip.quantity,
                p.name as part_name,
                c.name as color_name
            FROM inventories i
            JOIN inventory_parts ip ON i.id = ip.inventory_id
            JOIN parts p ON ip.part_num = p.part_num
            JOIN colors c ON ip.color_id = c.id
            WHERE i.set_num = ?
            ORDER BY ip.part_num, ip.color_id;
        """
        result = self.conn.execute(query, [set_num]).fetchall()
        return [dict(row) for row in result]

    def user_owns_set(self, id_user: int, set_num: str) -> bool:
        """
        Vérifie si un utilisateur possède un set donné.

        Paramètres :
        ------------
        id_user : int
            ID de l'utilisateur
        set_num : str
            Numéro du set

        Renvoie :
        ---------
        bool :
            True si l'utilisateur possède le set, False sinon
        """
        query = """
            SELECT COUNT(*) as count
            FROM user_owned_sets
            WHERE id_user = ? AND set_num = ?;
        """
        result = self.conn.execute(query, [id_user, set_num]).fetchone()
        return result["count"] > 0 if result else False

    def get_set_from_catalog(self, set_num: str) -> Set | None:
        """Récupère un set du catalogue Rebrickable"""
        query = "SELECT * FROM sets WHERE set_num = ?;"
        result = self.conn.execute(query, [set_num]).fetchone()
        return Set.from_dict(dict(result)) if result else None

    def get_user_owned_set(self, id_user: int, set_num: str) -> UserOwnedSet | None:
        """Récupère la relation user-set (sans détails du set)"""
        query = "SELECT * FROM user_owned_sets WHERE id_user = ? AND set_num = ?;"
        result = self.conn.execute(query, [id_user, set_num]).fetchone()
        return UserOwnedSet.from_dict(dict(result)) if result else None

    def get_user_sets_with_details(self, id_user: int) -> list[UserSetWithDetails]:
        """Récupère tous les sets d'un utilisateur avec détails (JOIN)"""
        query = """
            SELECT
                uos.id_user,
                uos.set_num,
                uos.is_built,
                s.name,
                s.year,
                s.theme_id,
                s.num_parts,
                s.img_url
            FROM user_owned_sets uos
            JOIN sets s ON uos.set_num = s.set_num
            WHERE uos.id_user = ?
            ORDER BY s.name;
        """
        result = self.conn.execute(query, [id_user]).fetchall()
        return [UserSetWithDetails.from_dict(dict(row)) for row in result]
