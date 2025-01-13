from profile import Profile


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.profile = None

    def set_profile(self, name, weight):
        if not self.profile:
            new_profile = Profile.create_profile(name, weight)
            self.profile = new_profile

    def update_password(self, new_password):
        self.password = new_password