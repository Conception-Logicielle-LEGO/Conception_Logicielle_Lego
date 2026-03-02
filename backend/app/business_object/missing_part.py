"""
DTO pour les pièces manquantes d'un set
Utilisé par l'algorithme de matching
"""

from dataclasses import dataclass


@dataclass
class MissingPart:
    """
    DTO pour représenter une pièce manquante pour construire un set.

    Utilisé par MatchingService pour détailler exactement quelles pièces
    l'utilisateur doit acquérir pour compléter un set.
    """

    # Identification de la pièce
    part_num: str
    color_id: int

    # Quantités
    needed: int  # Quantité nécessaire pour le set
    owned: int  # Quantité possédée par l'utilisateur
    missing: int  # Quantité manquante (needed - owned)

    # Détails catalogue (enrichi)
    part_name: str | None = None
    color_name: str | None = None
    color_rgb: str | None = None

    def __str__(self) -> str:
        color_info = f" ({self.color_name})" if self.color_name else ""
        name = self.part_name or self.part_num
        return f"❌ {self.missing}x {name}{color_info} (possède {self.owned}/{self.needed})"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer depuis un résultat de calcul SQL"""
        return cls(
            part_num=data["part_num"],
            color_id=data["color_id"],
            needed=data["needed"],
            owned=data.get("owned", 0),
            missing=data["missing"],
            part_name=data.get("part_name"),
            color_name=data.get("color_name"),
            color_rgb=data.get("color_rgb"),
        )

    def to_dict(self) -> dict:
        """Pour JSON API"""
        result = {
            "part_num": self.part_num,
            "color_id": self.color_id,
            "quantity": {
                "needed": self.needed,
                "owned": self.owned,
                "missing": self.missing,
            },
        }

        # Ajouter les détails si disponibles
        if self.part_name or self.color_name:
            result["details"] = {
                "part_name": self.part_name,
                "color_name": self.color_name,
                "color_rgb": f"#{self.color_rgb}" if self.color_rgb else None,
            }

        return result

    def is_completely_missing(self) -> bool:
        """Vérifie si l'utilisateur ne possède aucune instance de cette pièce"""
        return self.owned == 0

    def get_completion_percentage(self) -> float:
        """Calcule le pourcentage de cette pièce possédée"""
        if self.needed == 0:
            return 100.0
        return (self.owned / self.needed) * 100
