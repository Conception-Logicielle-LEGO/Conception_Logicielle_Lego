from datetime import datetime


class Wishlist:
    def __init__(
        self,
        id_user: int,
        id_wishlist: int | None = None,
        created_at: datetime | None = None,
    ):
        self.id_wishlist = id_wishlist
        self.id_user = id_user
        self.created_at = created_at

    def __str__(self) -> str:
        return f"Wishlist(id={self.id_wishlist}, user={self.id_user})"

    @classmethod
    def from_dict(cls, data: dict):
        """
        Création d'une Wishlist depuis la base de données
        """
        return cls(
            id_wishlist=data.get("id_wishlist"),
            id_user=data.get("id_user"),
            created_at=data.get("created_at"),
        )

    def to_dict(self):
        """
        Représentation minimale pour la persistance
        """
        return {
            "id_wishlist": self.id_wishlist,
            "id_user": self.id_user,
            "created_at": self.created_at,
        }
