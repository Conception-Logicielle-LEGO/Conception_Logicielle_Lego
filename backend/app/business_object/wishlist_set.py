"""
Business Object pour wishlist_sets
Table PostgreSQL: wishlist_sets
"""

from datetime import datetime


class WishlistSet:
    """
    Représente un set dans la wishlist d'un utilisateur.
    Table source : wishlist_sets
    """

    def __init__(
        self,
        id_wishlist: int,
        set_num: str,
        priority: int = 0,
        added_at: datetime | None = None,
    ):
        self.id_wishlist = id_wishlist  # FK vers wishlist
        self.set_num = set_num  # FK vers sets (DuckDB)
        self.priority = priority  # Priorité (0 = basse, plus élevé = plus important)
        self.added_at = added_at  # Date d'ajout à la wishlist

    def __str__(self) -> str:
        return f"WishlistSet {self.set_num} (priority={self.priority})"

    def __repr__(self) -> str:
        return (
            f"WishlistSet(id_wishlist={self.id_wishlist}, "
            f"set_num='{self.set_num}', priority={self.priority})"
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Créer un WishlistSet depuis un résultat SQL"""
        return cls(
            id_wishlist=data["id_wishlist"],
            set_num=data["set_num"],
            priority=data.get("priority", 0),
            added_at=data.get("added_at"),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "id_wishlist": self.id_wishlist,
            "set_num": self.set_num,
            "priority": self.priority,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }

    def increase_priority(self):
        """Augmenter la priorité du set"""
        self.priority += 1

    def decrease_priority(self):
        """Diminuer la priorité du set (minimum 0)"""
        self.priority = max(0, self.priority - 1)
