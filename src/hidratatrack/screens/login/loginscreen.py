import time
from pprint import pprint

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from models.models import session, User  # NoQA
from models.security import hash_password  # NoQA
from sqlalchemy.exc import SQLAlchemyError

from utils.snackbar_utils import show_snackbar


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def _validate_inputs(self, login, password):
        """Valida os campos de entrada antes de tentar autenticar"""
        if not login or not password:
            show_snackbar("Por favor, preencha todos os campos.")
            return False
        return True

    def _handle_successful_login(self, user):
        """Gerencia o fluxo após um login bem-sucedido"""
        self.app.user = user
        show_snackbar(f"Bem-vindo(a), {user.login}!")
        self.ids.password.text = ""

        self.app.switch_to_profile(user) if user.profiles == [] \
            else self.app.switch_to_tracker()

    def authenticate_user(self):
        """Realiza a autenticação do usuário com tratamento de erros"""
        try:
            login = self.ids.login.text.strip()
            password = self.ids.password.text
            if not self._validate_inputs(login, password):
                return
            user = session.query(User).filter_by(login=login).first()
            if user and user.password == hash_password(password):
                self._handle_successful_login(user)
            else:
                show_snackbar("Login ou senha inválidos.")
        except SQLAlchemyError as db_error:
            show_snackbar(
                "Erro ao conectar com o banco de dados. Tente novamente.")
            print(f"Erro de banco de dados: {str(db_error)}")
        except Exception as e:
            show_snackbar("Ocorreu um erro inesperado. Tente novamente.")
            print(f"Erro inesperado: {str(e)}")
