from datetime import datetime
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock

from user import User

# KivyMD Builder String for Layout
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    LoginScreen:
    CreateProfileScreen:
    TrackerScreen:
    SettingsScreen:

<LoginScreen>:
    name: "login"

    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "HidrataTrack"
            elevation: 4
            pos_hint: {"top": 1}
            md_bg_color: get_color_from_hex("#2196F3")

        MDFloatLayout:
            MDCard:
                size_hint: None, None
                size: "300dp", "400dp"
                pos_hint: {"center_x": .5, "center_y": .5}
                padding: "20dp"
                spacing: "20dp"
                elevation: 3
                
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "20dp"
                    adaptive_height: True
                    
                    MDLabel:
                        text: "Bem-vindo"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H4"
                        adaptive_height: True
                        
                    MDTextField:
                        id: login
                        hint_text: "Login"
                        helper_text: "Digite seu nome de usuário"
                        helper_text_mode: "on_focus"
                        icon_right: "account"
                        write_tab: False
                        
                    MDTextField:
                        id: password
                        hint_text: "Senha"
                        helper_text: "Digite sua senha"
                        helper_text_mode: "on_focus"
                        icon_right: "key-variant"
                        password: True
                        write_tab: False
                        
                    MDRaisedButton:
                        text: "Entrar"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#2196F3")
                        on_release: app.authenticate_user()
                        
                    MDRaisedButton:
                        text: "Criar Conta"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#4CAF50")
                        on_release: app.switch_to_create_account()
<CreateProfileScreen>:
    name: "create_profile"
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Criar Perfil"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.switch_to_menu()]]
            md_bg_color: get_color_from_hex("#2196F3")
            
        MDFloatLayout:
            MDCard:
                size_hint: None, None
                size: "500dp", "520dp"
                pos_hint: {"center_x": .5, "center_y": .5}
                padding: "20dp"
                spacing: "20dp"
                elevation: 3
                
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "20dp"
                    
                    MDLabel:
                        text: "Informações Pessoais"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H5"
                    
                    MDSegmentedControl:
                        id: gender_select
                        pos_hint: {"center_x": .5, "center_y": .5}
                        # size_hint_x: .7
                        on_active: app.on_gender_select(*args)
                        
                        MDSegmentedControlItem:
                            id: male
                            text: "Masculino"
                            
                        MDSegmentedControlItem:
                            id: female
                            text: "Feminino"

                    MDTextField:
                        id: name
                        hint_text: "Nome"
                        helper_text: "Digite seu nome completo"
                        helper_text_mode: "on_focus"
                        icon_right: "account"
                        write_tab: False
                        
                    DateField:
                        id: birth_date
                        hint_text: "Data de Nascimento"
                        helper_text: "Digite sua data de nascimento (DDMMAAAA)"
                        helper_text_mode: "on_focus"
                        icon_right: "calendar"
                        size_hint_y: None
                        height: self.minimum_height
                        write_tab: False
                        
                    MDTextField:
                        id: weight
                        hint_text: "Peso (kg)"
                        helper_text: "Digite seu peso em quilogramas"
                        helper_text_mode: "on_focus"
                        icon_right: "weight-kilogram"
                        input_filter: "float"
                        write_tab: False
                        
                    MDRaisedButton:
                        text: "Salvar Perfil"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#4CAF50")
                        on_release: app.create_profile()

<TrackerScreen>:
    name: "tracker"
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Controle Diário"
            elevation: 4
            right_action_items: [["cog", lambda x: app.switch_to_settings()]]
            md_bg_color: get_color_from_hex("#2196F3")
            
        MDFloatLayout:
            MDCard:
                size_hint: None, None
                size: "320dp", "500dp"
                pos_hint: {"center_x": .5, "center_y": .5}
                padding: "20dp"
                spacing: "20dp"
                elevation: 3
                
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "20dp"
                    
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
                        
                    MDProgressBar:
                        id: progress_bar
                        value: 0
                        color: get_color_from_hex("#2196F3")
                        size_hint_x: .9
                        pos_hint: {"center_x": .5}
                        
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        adaptive_height: True
                        pos_hint: {"center_x": .5}
                        
                        MDRaisedButton:
                            text: "100ml"
                            on_release: app.add_water(100)
                            md_bg_color: get_color_from_hex("#2196F3")
                            
                        MDRaisedButton:
                            text: "200ml"
                            on_release: app.add_water(200)
                            md_bg_color: get_color_from_hex("#2196F3")
                            
                        MDRaisedButton:
                            text: "300ml"
                            on_release: app.add_water(300)
                            md_bg_color: get_color_from_hex("#2196F3")
                    
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        adaptive_height: True
                        pos_hint: {"center_x": .5}
                        
                        MDRaisedButton:
                            text: "500ml"
                            on_release: app.add_water(500)
                            md_bg_color: get_color_from_hex("#4CAF50")
'''

class DateField(MDTextField):
    formatted_date = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = self.filter_date
        self._previous_value = ''
        
    def filter_date(self, value, boolean):
        # Remove qualquer caractere não numérico
        numbers = ''.join(filter(str.isdigit, value))
        
        if len(numbers) > 8:
            numbers = numbers[:8]
            
        # Formata a data conforme digita
        formatted = ''
        if len(numbers) > 0:
            formatted = numbers[:2]
        if len(numbers) > 2:
            formatted += '/' + numbers[2:4]
        if len(numbers) > 4:
            formatted += '/' + numbers[4:8]
            
        # Atualiza o texto do campo apenas se houver mudança
        if formatted != self._previous_value:
            self._previous_value = formatted
            Clock.schedule_once(lambda dt: self.update_text(formatted))
            
        return ''  # Retorna vazio pois vamos atualizar o texto via update_text
    
    def update_text(self, formatted_text):
        self.text = formatted_text
        self.formatted_date = formatted_text
        
    def get_date(self):
        """Converte a data formatada para objeto datetime"""
        try:
            if len(self.formatted_date) == 10:  # Formato completo DD/MM/YYYY
                return datetime.strptime(self.formatted_date, '%d/%m/%Y')
            return None
        except ValueError:
            return None

# Screens
class LoginScreen(MDScreen):
    pass

class CreateProfileScreen(MDScreen):
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
            if self.user.profile is None:
                self.switch_to_profile()
            else:
                self.switch_to_tracker()
        else:
            print("Login ou senha inválidos.")

    def create_profile(self):
        """Create a user profile and calculate the daily water goal."""
        user_name = self.sm.get_screen("create_profile").ids.name.text
        birth_date_field = self.sm.get_screen("create_profile").ids.birth_date
        weight = self.sm.get_screen("create_profile").ids.weight.text

        # Validação da data
        birth_date = birth_date_field.get_date()
        if not birth_date:
            self.show_snackbar("Data de nascimento inválida")
            return
        
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

    def switch_to_profile(self):
        """Switch to the profile screen."""
        self.sm.current = "create_profile"

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
    
    def on_gender_select(self, segmentedcontrol, segmentedcontrolitem):
        self.selected_gender = segmentedcontrolitem.text
        self.show_snackbar(f"Gênero selecionado: {self.selected_gender}")

    def show_snackbar(self, msg):
        print(msg)

if __name__ == "__main__":
    HidrataTrackApp().run()
