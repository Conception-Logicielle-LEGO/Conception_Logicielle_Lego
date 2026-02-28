# app/business_object/set.py


class Set:
    """
    Représente un set LEGO du catalogue Rebrickable.
    Table source : sets
    """

    def __init__(
        self,
        set_num: str,
        name: str,
        year: int,
        theme_id: int,
        num_parts: int,
        img_url: str | None = None,
    ):
        self.set_num = set_num  # PK - ex: "75192-1"
        self.name = name  # ex: "Millennium Falcon"
        self.year = year  # ex: 2017
        self.theme_id = theme_id  # FK vers themes
        self.num_parts = num_parts  # ex: 7541
        self.img_url = img_url  # URL de l'image

    def __str__(self) -> str:
        return (
            f"Set {self.set_num}: {self.name} ({self.year}) - {self.num_parts} pièces"
        )

    def __repr__(self) -> str:
        return f"Set(set_num='{self.set_num}', name='{self.name}')"

    @classmethod
    def from_dict(cls, data: dict):
        """Créer un Set depuis un résultat SQL"""
        return cls(
            set_num=data["set_num"],
            name=data["name"],
            year=data["year"],
            theme_id=data["theme_id"],
            num_parts=data["num_parts"],
            img_url=data.get("img_url"),  # Peut être NULL
        )

    def to_dict(self) -> dict:
        """Convertir en dictionnaire (pour JSON API)"""
        return {
            "set_num": self.set_num,
            "name": self.name,
            "year": self.year,
            "theme_id": self.theme_id,
            "num_parts": self.num_parts,
            "img_url": self.img_url,
        }
