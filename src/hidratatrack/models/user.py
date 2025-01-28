from src.hidratatrack.models.models import Profile


class AppUser:
    def __init__(self, login, email, password):
        self.login = login
        self.password = password
        self.email = email
        self.profile = None

    def set_profile(self, user):
        if not self.profile:
            new_profile = Profile(**user)
            self.profile = new_profile

    def update_password(self, new_password):
        self.password = new_password
