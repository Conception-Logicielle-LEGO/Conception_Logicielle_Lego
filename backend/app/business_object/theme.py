"""
Business Object pour themes
Table DuckDB (Rebrickable): themes
"""


class Theme:
    """
    Représente un thème LEGO du catalogue Rebrickable.
    Table source : themes (DuckDB - read-only)

    Les thèmes sont hiérarchiques (parent_id peut référencer un autre thème).
    Exemples: "Star Wars", "Harry Potter", "Architecture"
    """

    def __init__(
        self,
        id: int,
        name: str,
        parent_id: int | None = None,
    ):
        self.id = id  # PK - ex: 158 (Star Wars), 246 (Harry Potter)
        self.name = name  # ex: "Star Wars", "Episode IV, V, VI"
        self.parent_id = parent_id  # FK vers themes (nullable, pour sous-thèmes)

    def __str__(self) -> str:
        parent = f" (parent={self.parent_id})" if self.parent_id else ""
        return f"Theme {self.name}{parent}"

    def __repr__(self) -> str:
        return f"Theme(id={self.id}, name='{self.name}')"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer un Theme depuis un résultat SQL"""
        return cls(
            id=data["id"],
            name=data["name"],
            parent_id=data.get("parent_id"),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
        }

    def is_sub_theme(self) -> bool:
        """Vérifie si c'est un sous-thème (a un parent)"""
        return self.parent_id is not None

    def is_root_theme(self) -> bool:
        """Vérifie si c'est un thème racine (sans parent)"""
        return self.parent_id is None
