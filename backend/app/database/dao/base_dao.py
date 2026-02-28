from abc import ABC, abstractmethod


class BaseDAO(ABC):
    """
    Classe de base abstraite pour tous les DAO.
    Fournit des méthodes génériques réutilisables.
    """

    def __init__(self, db_connection):
        self.conn = db_connection(read_only=False)

    @abstractmethod
    def get_table_name(self) -> str:
        """
        Retourne le nom de la table principale gérée par ce DAO.
        Doit être implémenté par chaque DAO enfant pour préciser les colonnes.
        """
        pass

    @abstractmethod
    def get_allowed_columns(self) -> set[str]:
        """
        Retourne l'ensemble des colonnes autorisées pour les requêtes get_by().
        Liste blanche pour éviter les injections SQL.
        Doit être implémenté par chaque DAO enfant.
        """
        pass

    @abstractmethod
    def from_row(self, row: dict):
        """
        Convertit une ligne SQL (dict) en objet métier.
        Doit être implémenté par chaque DAO enfant.

        Exemple pour UserDAO :
            return User.from_dict(row)
        """
        pass

    def get_by(self, column: str, value) -> list:
        """
        Récupère des entités depuis la base de données selon une colonne donnée.

        Cette fonction effectue une requête sécurisée pour éviter les injections SQL
        en utilisant une liste blanche des colonnes autorisées (définie dans get_allowed_columns).

        Paramètres :
        -----------
        column : str
            Nom de la colonne à filtrer (doit être dans get_allowed_columns())
        value : Any
            Valeur à chercher dans la colonne spécifiée

        Renvoie :
        ---------
        list :
            Liste d'objets métier correspondant aux critères.
            La liste peut être vide si aucune entité ne correspond.

        Lève :
        ------
        ValueError :
            Si la colonne passée en paramètre n'est pas autorisée

        Exemple :
        ---------
        >>> user_dao = UserDAO(db_connection)
        >>> users = user_dao.get_by("username", "john_doe")
        >>> sets = set_dao.get_by("id_user", 42)
        """
        # Vérification liste blanche
        if column not in self.get_allowed_columns():
            raise ValueError(
                f"Colonne '{column}' non autorisée pour {self.__class__.__name__}. "
                f"Colonnes autorisées : {self.get_allowed_columns()}"
            )

        query = f"""
            SELECT *
            FROM {self.get_table_name()}
            WHERE {column} = ?;
        """

        result = self.conn.execute(query, [value]).fetchall()

        # Conversion des lignes en objets métier
        return [self.from_row(dict(row)) for row in result]

    def get_all(self) -> list:
        """
        Récupère toutes les entités de la table.

        Renvoie :
        ---------
        list :
            Liste de tous les objets métier de la table
        """
        query = f"SELECT * FROM {self.get_table_name()};"
        result = self.conn.execute(query).fetchall()
        return [self.from_row(dict(row)) for row in result]

    def exists(self, column: str, value) -> bool:
        """
        Vérifie si une entité existe selon une colonne donnée.

        Paramètres :
        -----------
        column : str
            Nom de la colonne à filtrer (doit être dans get_allowed_columns())
        value : Any
            Valeur à chercher

        Renvoie :
        ---------
        bool :
            True si au moins une entité existe, False sinon

        Lève :
        ------
        ValueError :
            Si la colonne passée en paramètre n'est pas autorisée
        """
        if column not in self.get_allowed_columns():
            raise ValueError(
                f"Colonne '{column}' non autorisée pour {self.__class__.__name__}"
            )

        query = f"""
            SELECT COUNT(*) as count
            FROM {self.get_table_name()}
            WHERE {column} = ?;
        """

        result = self.conn.execute(query, [value]).fetchone()
        return result["count"] > 0 if result else False
