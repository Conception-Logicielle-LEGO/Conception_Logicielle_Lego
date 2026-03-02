"""
Business Object pour wishlist_parts
Table PostgreSQL: wishlist_parts
"""

from datetime import datetime


class WishlistPart:
    """
    Représente une pièce dans la wishlist d'un utilisateur.
    Table source : wishlist_parts
    """

    def __init__(
        self,
        id_wishlist: int,
        part_num: str,
        color_id: int,
        quantity: int = 1,
        added_at: datetime | None = None,
    ):
        self.id_wishlist = id_wishlist  # FK vers wishlist
        self.part_num = part_num  # FK vers parts (DuckDB)
        self.color_id = color_id  # FK vers colors (DuckDB)
        self.quantity = quantity  # Quantité souhaitée
        self.added_at = added_at  # Date d'ajout à la wishlist

    def __str__(self) -> str:
        return (
            f"WishlistPart {self.part_num} (color={self.color_id}, qty={self.quantity})"
        )

    def __repr__(self) -> str:
        return (
            f"WishlistPart(id_wishlist={self.id_wishlist}, "
            f"part_num='{self.part_num}', color_id={self.color_id})"
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Créer un WishlistPart depuis un résultat SQL"""
        return cls(
            id_wishlist=data["id_wishlist"],
            part_num=data["part_num"],
            color_id=data["color_id"],
            quantity=data.get("quantity", 1),
            added_at=data.get("added_at"),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "id_wishlist": self.id_wishlist,
            "part_num": self.part_num,
            "color_id": self.color_id,
            "quantity": self.quantity,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }
