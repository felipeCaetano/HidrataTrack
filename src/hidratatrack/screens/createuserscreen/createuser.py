from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from models.security import hash_password  # NoQA

from models.models import User
from utils.snackbar_utils import show_snackbar


class CreateUserScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.app = MDApp.get_running_app()

    def create_user(self):
        user_name = self.ids.login.text
        email = self.ids.email.text
        senha = self.ids.password.text
        if not all([user_name, email, senha]):
            show_snackbar("Por favor, preencha todos os campos.")
            return
        hashed_password = hash_password(senha)
        self.user = User(user_name, email, hashed_password)
        self.clear_fields()
        user_db = self.app.save_user(self.user)
        if user_db:
            self.switch_to_login()

    def clear_fields(self):
        self.ids.login.text = ''
        self.ids.email.text = ''
        self.ids.password.text = ''

    def switch_to_login(self):
        self.app.switch_to_login()
