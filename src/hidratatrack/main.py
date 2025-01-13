from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from user import User

# KivyMD Builder String for Layout
KV = '''
ScreenManager:
    LoginScreen:
    MenuScreen:
    TrackerScreen:
    SettingsScreen:

<LoginScreen>:
    name: "login"

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(20)

        MDLabel:
            text: "HidrataTrack"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H5"

        MDTextField:
            id: login
            hint_text: "Login"
            mode: "rectangle"
            write_tab: False

        MDTextField:
            id: password
            hint_text: "Senha"
            mode: "rectangle"
            password: True
            write_tab: False

        MDRaisedButton:
            text: "Entrar"
            pos_hint: {"center_x": 0.5}
            on_release: app.authenticate_user()

        MDRaisedButton:
            text: "Criar Conta"
            pos_hint: {"center_x": 0.5}
            on_release: app.switch_to_create_account()

<MenuScreen>:
    name: "menu"

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(20)

        MDLabel:
            text: "HidrataTrack"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H5"

        MDTextField:
            id: user_name
            hint_text: "Digite seu nome"
            mode: "rectangle"

        MDTextField:
            id: user_weight
            hint_text: "Digite seu peso (kg)"
            mode: "rectangle"
            input_filter: "float"

        MDRaisedButton:
            text: "Criar Perfil"
            pos_hint: {"center_x": 0.5}
            on_release: app.create_profile()

        MDRaisedButton:
            text: "Ir para Rastreamento"
            pos_hint: {"center_x": 0.5}
            on_release: app.switch_to_tracker()

<TrackerScreen>:
    name: "tracker"

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(20)

        MDLabel:
            id: daily_goal_label
            text: "Meta Diária: 0 ml"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H6"

        MDLabel:
            id: progress_label
            text: "Progresso: 0 ml"
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            text: "Adicionar 200ml"
            pos_hint: {"center_x": 0.5}
            on_release: app.add_water(200)

        MDRaisedButton:
            text: "Voltar para Menu"
            pos_hint: {"center_x": 0.5}
            on_release: app.switch_to_menu()

<SettingsScreen>:
    name: "settings"

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(20)

        MDTextField:
            id: new_weight
            hint_text: "Atualizar Peso (kg)"
            mode: "rectangle"
            input_filter: "float"

        MDRaisedButton:
            text: "Salvar Peso"
            pos_hint: {"center_x": 0.5}
            on_release: app.update_weight()

        MDRaisedButton:
            text: "Voltar para Menu"
            pos_hint: {"center_x": 0.5}
            on_release: app.switch_to_menu()
'''

# Screens
class LoginScreen(MDScreen):
    pass

class MenuScreen(MDScreen):
    pass

class TrackerScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass

class HidrataTrackApp(MDApp):
    def build(self):
        self.user = None  # Placeholder for user data
        self.daily_goal = 0
        self.progress = 0

        self.sm = Builder.load_string(KV)
        return self.sm
    
    def authenticate_user(self):
        login = self.sm.get_screen("login").ids.login.text
        password = self.sm.get_screen("login").ids.password.text

        # Placeholder for authentication logic
        if login == "test" and password == "1234":
            self.user = User(login, password)
            print("Usuário autenticado com sucesso!")
            self.switch_to_tracker()
        else:
            print("Login ou senha inválidos.")

    def create_profile(self):
        """Create a user profile and calculate the daily water goal."""
        user_name = self.sm.get_screen("menu").ids.user_name.text
        user_weight = self.sm.get_screen("menu").ids.user_weight.text

        if not user_name or not user_weight:
            print("Por favor, preencha todos os campos.")
            return

        self.user = {
            "name": user_name,
            "weight": float(user_weight),
        }
        self.daily_goal = (float(user_weight) / 20) * 1000
        print(f"Perfil criado: {self.user}")

    def switch_to_create_account(self):
        ...

    def switch_to_tracker(self):
        """Switch to the tracker screen."""
        if not self.user:
            print("Por favor, crie um perfil antes.")
            return

        tracker_screen = self.sm.get_screen("tracker")
        tracker_screen.ids.daily_goal_label.text = f"Meta Diária: {self.daily_goal} ml"
        tracker_screen.ids.progress_label.text = f"Progresso: {self.progress} ml"
        self.sm.current = "tracker"

    def add_water(self, amount):
        """Add water to the progress and update the tracker screen."""
        self.progress += amount
        tracker_screen = self.sm.get_screen("tracker")
        tracker_screen.ids.progress_label.text = f"Progresso: {self.progress} ml"

    def switch_to_menu(self):
        """Switch to the menu screen."""
        self.sm.current = "menu"

    def update_weight(self):
        """Update the user's weight and recalculate the daily goal."""
        new_weight = self.sm.get_screen("settings").ids.new_weight.text

        if not new_weight or not self.user:
            print("Peso inválido ou perfil não criado.")
            return

        self.user["weight"] = float(new_weight)
        self.daily_goal = (float(new_weight) / 20) * 1000
        print(f"Peso atualizado: {self.user['weight']} kg, Nova meta: {self.daily_goal} ml")
        self.sm.current = "menu"

if __name__ == "__main__":
    HidrataTrackApp().run()
