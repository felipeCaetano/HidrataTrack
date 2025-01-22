import hashlib
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from sqlalchemy.exc import SQLAlchemyError

from models.models import session, User


class LoginScreen(MDScreen):
   def __init__(self, **kwargs):
      super(LoginScreen, self).__init__(**kwargs)
      self.app = MDApp.get_running_app()
      # self.ids.login.text = ""
      # self.ids.password.text = ""

   def _hash_password(self, password):
      """Cria um hash seguro da senha usando SHA-256"""
      return hashlib.sha256(password.encode()).hexdigest()
   
   def _validate_inputs(self, login, password):
      """Valida os campos de entrada antes de tentar autenticar"""
      if not login or not password:
         self.app.show_snackbar("Por favor, preencha todos os campos.")
         return False
      return True

   def _handle_successful_login(self, user):
      """Gerencia o fluxo após um login bem-sucedido"""
      self.app.user = user
      self.app.show_snackbar(f"Bem-vindo(a), {user.login}!")
      
      # Limpa os campos de senha por segurança
      self.ids.password.text = ""
      
      # Decide para qual tela navegar
      if not user.profiles:  # usando not ao invés de is None para mais flexibilidade
         self.app.switch_to_profile(user)
      else:
         self.app.switch_to_tracker()

   def authenticate_user(self):
      """Realiza a autenticação do usuário com tratamento de erros"""
      try:
         login = self.ids.login.text.strip()
         password = self.ids.password.text
         if not self._validate_inputs(login, password):
            return
         user = session.query(User).filter_by(login=login).first()
         if user and user.password == self._hash_password(password):
            self._handle_successful_login(user)
         else:
             self.app.show_snackbar("Login ou senha inválidos.")
      except SQLAlchemyError as db_error:
         self.app.show_snackbar("Erro ao conectar com o banco de dados. Tente novamente.")
         print(f"Erro de banco de dados: {str(db_error)}")
      except Exception as e:
         self.app.show_snackbar("Ocorreu um erro inesperado. Tente novamente.")
         print(f"Erro inesperado: {str(e)}")
        