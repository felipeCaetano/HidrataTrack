from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from models.models import session, User
from models.user import AppUser


class LoginScreen(MDScreen):
   def __init__(self, **kwargs):
      super(LoginScreen, self).__init__(**kwargs)
      self.app = MDApp.get_running_app()

   def authenticate_user(self):
      login = self.ids.login.text
      password = self.ids.password.text
      user = session.query(User).filter_by(login=login).first()
      # Placeholder for authentication logic
      if user and user.password == password:
         self.app.user = user
         self.app.show_snackbar(f"{login} logado com sucesso.")
         if self.app.user.profiles is None:
            self.app.switch_to_profile(user)
         else:
            self.app.switch_to_tracker()
      else:
         self.app.show_snackbar("Login ou senha inválidos.")