"""BO représentant un set favori d'un utilisateur."""


class FavoriteSet:
    """
    Représente un set LEGO mis en favori par un utilisateur.
    Table source : favorite_sets
    """

    def __init__(self, id_user: int, set_num: str, added_at=None):
        self.id_user = id_user
        self.set_num = set_num
        self.added_at = added_at

    def __str__(self) -> str:
        return f"FavoriteSet {self.set_num} (user={self.id_user})"

    def __repr__(self) -> str:
        return f"FavoriteSet(id_user={self.id_user}, set_num='{self.set_num}', added_at={self.added_at})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, FavoriteSet):
            return False
        return self.id_user == other.id_user and self.set_num == other.set_num

    @classmethod
    def from_dict(cls, data: dict) -> "FavoriteSet":
        """Créer un FavoriteSet depuis un résultat SQL."""
        return cls(
            id_user=data["id_user"],
            set_num=data["set_num"],
            added_at=data.get("added_at"),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)."""
        return {
            "id_user": self.id_user,
            "set_num": self.set_num,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }
