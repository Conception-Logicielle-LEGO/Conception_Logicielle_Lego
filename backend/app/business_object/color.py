"""
Business Object pour colors
Table DuckDB (Rebrickable): colors
"""


class Color:
    """
    Représente une couleur LEGO du catalogue Rebrickable.
    Table source : colors (DuckDB - read-only)
    """

    def __init__(
        self,
        id: int,
        name: str,
        rgb: str,
        is_trans: bool = False,
    ):
        self.id = id  # PK - ex: 0 (Black), 1 (Blue), etc.
        self.name = name  # ex: "Black", "Blue", "Trans-Clear"
        self.rgb = rgb  # ex: "05131D" (code hexa sans #)
        self.is_trans = is_trans  # Transparent ?

    def __str__(self) -> str:
        trans = " (transparent)" if self.is_trans else ""
        return f"Color {self.name} #{self.rgb}{trans}"

    def __repr__(self) -> str:
        return f"Color(id={self.id}, name='{self.name}', rgb='{self.rgb}')"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer un Color depuis un résultat SQL"""
        return cls(
            id=data["id"],
            name=data["name"],
            rgb=data["rgb"],
            is_trans=data.get("is_trans", False),
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "id": self.id,
            "name": self.name,
            "rgb": self.rgb,
            "is_trans": self.is_trans,
        }

    def get_hex_color(self) -> str:
        """Retourne le code couleur avec # pour usage CSS"""
        return f"#{self.rgb}"
