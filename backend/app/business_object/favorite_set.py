"""
Business Object pour favorite_sets
Table PostgreSQL: favorite_sets
"""

from datetime import datetime


class FavoriteSet:
    """
    Représente un set favori d'un utilisateur.
    Table source : favorite_sets
    """

    def __init__(
        self,
        id_user: int,
        set_num: str,
        added_at: datetime | None = None,
    ):
        self.id_user = id_user  # FK vers users
        self.set_num = set_num  # FK vers sets (DuckDB)
        self.added_at = added_at  # Date d'ajout aux favoris

    def __str__(self) -> str:
        return f"FavoriteSet {self.set_num} (user={self.id_user})"

    def __repr__(self) -> str:
        return f"FavoriteSet(id_user={self.id_user}, set_num='{self.set_num}')"

    @classmethod
    def from_dict(cls, data: dict) -> "FavoriteSet":
        """Créer un FavoriteSet depuis un résultat SQL"""
        return cls(
            id_user=data["id_user"],
            set_num=data["set_num"],
            added_at=data.get("added_at"),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "id_user": self.id_user,
            "set_num": self.set_num,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }

    def __eq__(self, other) -> bool:
        """Compare deux FavoriteSet (utile pour les tests)."""
        if not isinstance(other, FavoriteSet):
            return False
        return self.id_user == other.id_user and self.set_num == other.set_num
