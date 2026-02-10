class Set:
    def __init__(
        self,
        set_num: str,
        id_user: int | None = None,
    ):
        self.id_user = id_user
        self.set_num = set_num

    def __str__(self) -> str:
        return f"OwnedSet {self.set_num} (user={self.id_user})"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_user=data.get("id_user"),
            set_num=data.get("set_num"),
        )

    def to_dict(self):
        """
        À utiliser UNIQUEMENT pour la persistance
        """
        return {
            "id_user": self.id_user,
            "set_num": self.set_num,
        }
