class User:
    def __init__(self, username, hashed_password, salt, id_user=None):
        self.id_user = id_user
        self.username = username
        self.hashed_password = hashed_password
        self.salt = salt

    def __str__(self) -> str:
        return f"{self.username} (id={self.id_user})"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_user=data.get("id_user"),
            username=data.get("username"),
            hashed_password=data.get("hashed_password"),
            salt=data.get("salt"),
        )

    def to_dict(self):
        """
        À utiliser UNIQUEMENT pour la persistance
        """
        return {
            "id_user": self.id_user,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "salt": self.salt,
        }
