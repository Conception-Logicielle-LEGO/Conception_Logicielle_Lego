"""
DTO enrichi pour l'affichage des pièces de wishlist avec détails complets
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WishlistPartWithDetails:
    """
    DTO (Data Transfer Object) enrichi pour l'API.
    Combine les données de wishlist_parts + parts + colors (JOIN SQL).

    Utilisé pour retourner à l'API la liste complète des pièces souhaitées
    d'un utilisateur avec tous les détails (nom, couleur, etc.).
    """

    # Données wishlist_parts
    id_wishlist: int
    part_num: str
    color_id: int
    quantity: int
    added_at: datetime | None = None

    # Données parts (catalogue)
    part_name: str
    part_cat_id: int

    # Données colors (catalogue)
    color_name: str
    color_rgb: str
    is_trans: bool

    def __str__(self) -> str:
        return f"★ {self.quantity}x {self.part_name} ({self.color_name})"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer depuis un résultat de JOIN SQL"""
        return cls(
            # wishlist_parts
            id_wishlist=data["id_wishlist"],
            part_num=data["part_num"],
            color_id=data["color_id"],
            quantity=data["quantity"],
            added_at=data.get("added_at"),
            # parts
            part_name=data["part_name"],
            part_cat_id=data["part_cat_id"],
            # colors
            color_name=data["color_name"],
            color_rgb=data["color_rgb"],
            is_trans=data["is_trans"],
        )

    def to_dict(self) -> dict:
        """Pour JSON API"""
        return {
            "wishlist": {
                "id_wishlist": self.id_wishlist,
                "quantity": self.quantity,
                "added_at": self.added_at.isoformat() if self.added_at else None,
            },
            "part": {
                "part_num": self.part_num,
                "name": self.part_name,
                "category_id": self.part_cat_id,
            },
            "color": {
                "id": self.color_id,
                "name": self.color_name,
                "rgb": f"#{self.color_rgb}",
                "is_transparent": self.is_trans,
            },
        }
