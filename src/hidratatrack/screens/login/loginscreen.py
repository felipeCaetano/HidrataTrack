from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from services.auth import authenticate_user # NoQA
from services.events import EventEmitter    # NoQA
from utils.snackbar_utils import show_snackbar  # NoQA


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.events = EventEmitter()
        # Registra handlers para os eventos
        self.events.on("login_failed", self.handle_login)
        self.events.on("database_warning", self.handle_login)
        self.events.on("warning", self.handle_login)

    def _validate_inputs(self, login, password):
        """Valida os campos de entrada antes de tentar autenticar"""
        if not login or not password:
            show_snackbar("Por favor, preencha todos os campos.")
            return False
        return True

    def _handle_successful_login(self, user, profiles):
        """Gerencia o fluxo após um login bem-sucedido"""
        self.app.user = user
        self.app.user.profiles = profiles
        show_snackbar(f"Bem-vindo(a), {user.login}!")
        self.ids.password.text = ""

        self.app.switch_to_profile(user) if user.profiles == [] \
            else self.app.switch_to_tracker()

    def handle_auth(self):
        """Realiza a autenticação do usuário com tratamento de erros"""
        login = self.ids.login.text.strip()
        password = self.ids.password.text
        if not self._validate_inputs(login, password):
            return
        user, profile = authenticate_user(login, password)
        if user:
            self._handle_successful_login(user, profile)

    def handle_login(self, msg: str):
        show_snackbar(msg)

    def handle_forgot_password(self):
        pass
        
