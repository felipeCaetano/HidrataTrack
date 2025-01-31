from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from models.models import session
 # NoQA
from services.user_service import create_user, save_user
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
        self.user = create_user(user_name, email, senha)
        self.clear_fields()
        user_db = save_user(self.user, session)
        if user_db:
            self.switch_to_login()

    def clear_fields(self):
        self.ids.login.text = ''
        self.ids.email.text = ''
        self.ids.password.text = ''

    def switch_to_login(self):
        self.app.switch_to_login()
