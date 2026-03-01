"""
DTO enrichi pour l'affichage des pièces avec détails complets
"""

from dataclasses import dataclass


@dataclass
class PartWithDetails:
    """
    DTO (Data Transfer Object) enrichi pour l'API.
    Combine les données de user_parts + parts + colors (JOIN SQL).

    Utilisé pour retourner à l'API la liste complète des pièces
    d'un utilisateur avec tous les détails (nom, couleur, etc.).
    """

    # Données user_parts
    id_user: int
    part_num: str
    color_id: int
    quantity: int
    status: str  # 'owned' ou 'wished'
    is_used: bool

    # Données parts (catalogue)
    part_name: str
    part_cat_id: int

    # Données colors (catalogue)
    color_name: str
    color_rgb: str
    is_trans: bool

    def __str__(self) -> str:
        status_icon = "✓" if self.status == "owned" else "★"
        used = " [USED]" if self.is_used else ""
        return (
            f"{status_icon} {self.quantity}x {self.part_name} ({self.color_name}){used}"
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Créer depuis un résultat de JOIN SQL"""
        return cls(
            # user_parts
            id_user=data["id_user"],
            part_num=data["part_num"],
            color_id=data["color_id"],
            quantity=data["quantity"],
            status=data["status"],
            is_used=data["is_used"],
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
            "user": {
                "id_user": self.id_user,
                "quantity": self.quantity,
                "status": self.status,
                "is_used": self.is_used,
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

    def is_owned(self) -> bool:
        """Vérifie si la pièce est possédée"""
        return self.status == "owned"

    def is_wished(self) -> bool:
        """Vérifie si la pièce est souhaitée"""
        return self.status == "wished"
