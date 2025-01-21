from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from models.user import AppUser


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
            self.app.show_snackbar("Por favor, preencha todos os campos.")
            return
        self.user = AppUser(user_name, email, senha)
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