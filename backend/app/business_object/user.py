class User:
    # constructeur
    def __init__(self, username, password, salt=None, id_user=None):
        self.username = username
        self.id_user = id_user
        self.password = password
        self.salt = salt
