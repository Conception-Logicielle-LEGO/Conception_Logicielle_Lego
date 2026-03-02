"""
Business Object pour user_parts
Table PostgreSQL: user_parts
"""

from datetime import datetime


class UserPart:
    """
    Représente une pièce possédée ou souhaitée par un utilisateur.
    Table source : user_parts

    Cette classe gère à la fois:
    - Les pièces possédées (status='owned')
    - Les pièces souhaitées (status='wished')
    """

    def __init__(
        self,
        id_user: int,
        part_num: str,
        color_id: int,
        quantity: int = 1,
        status: str = "owned",
        is_used: bool = False,
        added_at: datetime | None = None,
    ):
        self.id_user = id_user  # FK vers users
        self.part_num = part_num  # FK vers parts (DuckDB)
        self.color_id = color_id  # FK vers colors (DuckDB)
        self.quantity = quantity  # Quantité possédée/souhaitée
        self.status = status  # 'owned' ou 'wished'
        self.is_used = is_used  # Pièce utilisée dans un set construit
        self.added_at = added_at  # Date d'ajout

    def __str__(self) -> str:
        return (
            f"UserPart {self.part_num} (color={self.color_id}, "
            f"qty={self.quantity}, status={self.status}, used={self.is_used})"
        )

    def __repr__(self) -> str:
        return (
            f"UserPart(id_user={self.id_user}, part_num='{self.part_num}', "
            f"color_id={self.color_id}, status='{self.status}')"
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Créer un UserPart depuis un résultat SQL"""
        return cls(
            id_user=data["id_user"],
            part_num=data["part_num"],
            color_id=data["color_id"],
            quantity=data.get("quantity", 1),
            status=data.get("status", "owned"),
            is_used=data.get("is_used", False),
            added_at=data.get("added_at"),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "id_user": self.id_user,
            "part_num": self.part_num,
            "color_id": self.color_id,
            "quantity": self.quantity,
            "status": self.status,
            "is_used": self.is_used,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }

    def is_owned(self) -> bool:
        """Vérifie si la pièce est possédée"""
        return self.status == "owned"

    def is_wished(self) -> bool:
        """Vérifie si la pièce est souhaitée"""
        return self.status == "wished"

    def mark_as_used(self):
        """Marquer la pièce comme utilisée dans un set"""
        self.is_used = True

    def mark_as_free(self):
        """Marquer la pièce comme libre (non utilisée)"""
        self.is_used = False

    def add_quantity(self, qty: int):
        """Ajouter une quantité de pièces"""
        self.quantity += qty

    def remove_quantity(self, qty: int):
        """Retirer une quantité de pièces (minimum 0)"""
        self.quantity = max(0, self.quantity - qty)
