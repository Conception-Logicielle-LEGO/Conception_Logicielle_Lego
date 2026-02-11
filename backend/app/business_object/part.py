class Part:
    def __init__(
        self,
        part_num: str,
        status_owned_wished: str,
        is_used: bool,
        id_user: int | None = None,
    ):
        self.id_user = id_user
        self.part_num = part_num
        self.status_owned_wished = status_owned_wished
        self.is_used = is_used

    def __str__(self) -> str:
        return (
            f"Part {self.part_num} "
            f"(user={self.id_user}, status={self.status_owned_wished}, used={self.is_used})"
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_user=data.get("id_user"),
            part_num=data.get("part_num"),
            status_owned_wished=data.get("status_owned_wished"),
            is_used=data.get("is_used"),
        )

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "part_num": self.part_num,
            "status_owned_wished": self.status_owned_wished,
            "is_used": self.is_used,
        }
