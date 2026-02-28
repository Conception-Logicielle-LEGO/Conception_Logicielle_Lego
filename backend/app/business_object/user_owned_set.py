from dataclasses import dataclass


class UserOwnedSet:
    """
    Représente un set LEGO possédé par un utilisateur.
    Table source : user_owned_sets

    Cette classe fait le lien entre un utilisateur et un set du catalogue.
    """

    def __init__(
        self,
        id_user: int,
        set_num: str,
        is_built: bool = False,
    ):
        self.id_user = id_user  # FK vers users
        self.set_num = set_num  # FK vers sets
        self.is_built = is_built  # Statut de construction

    def __str__(self) -> str:
        status = "construit" if self.is_built else "non construit"
        return f"UserOwnedSet {self.set_num} (user={self.id_user}, {status})"

    def __repr__(self) -> str:
        return f"UserOwnedSet(id_user={self.id_user}, set_num='{self.set_num}', is_built={self.is_built})"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer un UserOwnedSet depuis un résultat SQL"""
        return cls(
            id_user=data["id_user"],
            set_num=data["set_num"],
            is_built=data.get("is_built", False),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "id_user": self.id_user,
            "set_num": self.set_num,
            "is_built": self.is_built,
        }

    def mark_as_built(self):
        """Marquer le set comme construit"""
        self.is_built = True

    def mark_as_unbuilt(self):
        """Marquer le set comme non construit"""
        self.is_built = False


@dataclass
class UserSetWithDetails:
    """
    DTO (Data Transfer Object) enrichi pour l'API.
    Combine les données de user_owned_sets + sets (JOIN SQL).

    Utilisé pour retourner à l'API la liste complète des sets
    d'un utilisateur avec tous les détails.
    """

    # Données user_owned_sets
    id_user: int
    set_num: str
    is_built: bool

    # Données sets (catalogue)
    name: str
    year: int
    theme_id: int
    num_parts: int
    img_url: str | None = None

    def __str__(self) -> str:
        status = "✓" if self.is_built else "✗"
        return f"{status} {self.name} ({self.set_num}) - {self.num_parts} pièces"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer depuis un résultat de JOIN SQL"""
        return cls(
            id_user=data["id_user"],
            set_num=data["set_num"],
            is_built=data["is_built"],
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
                "is_built": self.is_built,
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
