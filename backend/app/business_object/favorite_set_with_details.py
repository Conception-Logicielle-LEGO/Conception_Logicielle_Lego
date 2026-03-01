"""
DTO enrichi pour l'affichage des sets favoris avec détails complets
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class FavoriteSetWithDetails:
    """
    DTO (Data Transfer Object) enrichi pour l'API.
    Combine les données de favorite_sets + sets (JOIN SQL).

    Utilisé pour retourner à l'API la liste complète des sets favoris
    d'un utilisateur avec tous les détails du catalogue.
    """

    # Données favorite_sets
    id_user: int
    set_num: str
    added_at: datetime | None = None

    # Données sets (catalogue)
    name: str
    year: int
    theme_id: int
    num_parts: int
    img_url: str | None = None

    def __str__(self) -> str:
        return f"❤️ {self.name} ({self.set_num}) - {self.num_parts} pièces"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer depuis un résultat de JOIN SQL"""
        return cls(
            # favorite_sets
            id_user=data["id_user"],
            set_num=data["set_num"],
            added_at=data.get("added_at"),
            # sets
            name=data["name"],
            year=data["year"],
            theme_id=data["theme_id"],
            num_parts=data["num_parts"],
            img_url=data.get("img_url"),
        )

    def to_dict(self) -> dict:
        """Pour JSON API"""
        return {
            "user": {
                "id_user": self.id_user,
                "added_at": self.added_at.isoformat() if self.added_at else None,
            },
            "set": {
                "set_num": self.set_num,
                "name": self.name,
                "year": self.year,
                "theme_id": self.theme_id,
                "num_parts": self.num_parts,
                "img_url": self.img_url,
            },
        }
