from models.perfil import Profile


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.profile = None

    def set_profile(self, user):
        if not self.profile:
            new_profile = Profile(**user)
            self.profile = new_profile

    def update_password(self, new_password):
        self.password = new_password