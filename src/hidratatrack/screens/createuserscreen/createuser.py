from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from services.user_service import create_user, save_user    # NoQA


class CreateUserScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.app = MDApp.get_running_app()

    def create_user(self):
        user_name = self.ids.login.text
        email = self.ids.email.text
        senha = self.ids.password.text
        self.user = create_user(user_name, email, senha)
        self.clear_fields()
        user_db = save_user(self.user)
        if user_db:
            self.switch_to_login()

    def clear_fields(self):
        self.ids.login.text = ''
        self.ids.email.text = ''
        self.ids.password.text = ''

    def switch_to_login(self):
        self.app.switch_to_login()
