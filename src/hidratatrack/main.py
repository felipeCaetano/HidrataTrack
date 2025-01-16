from datetime import datetime
from decimal import ROUND_UP, Decimal
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.clock import Clock

from user import User
from water_tracker import WaterTracker
from datefield import DateField

# KivyMD Builder String for Layout
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import DateField datefield

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
                        current_active_segment: male
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
                        helper_text: "Digite sua data de nascimento (DD/MM/AAAA)"
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
                    
                    MDTextField:
                        id: details
                        multiline: True
                        mode: "rectangle"
                        hint_text: "Detalhes adicionais"
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
                        text: "Meta Diária: 0 mL"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H6"
                        
                    MDLabel:
                        id: progress_label
                        text: "Progresso: 0 mL"
                        halign: "center"
                        theme_text_color: "Secondary"
                        
                    MDProgressBar:
                        id: progress_bar
                        value: 0
                        color: get_color_from_hex("#2196F3")
                        size_hint_x: .9
                        pos_hint: {"center_x": .5}
                        
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "10dp"
                        adaptive_height: True
                        pos_hint: {"center_x": .5}
                        
                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_height: True
                            spacing: "10dp"

                            MDTextField:
                                id: water_add
                                mode: "rectangle"
                                hint_text: "Volume bebido."
                                helper_text: "Digite o volume em mL"
                                helper_text_mode: "on_focus"
                                #icon_right: "water-plus"
                                input_filter: "float"
                                write_tab: False
                            
                            MDIconButton:
                                icon: "water-plus"
                                on_release: app.add_water(float(water_add.text))
                                md_bg_color: get_color_from_hex("#2196F3")
                        
                        MDWidget:

                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_height: True
                            spacing: "10dp"

                            MDFillRoundFlatIconButton:
                                icon: "cup-water"
                                text: "100ml"
                                on_release: app.add_water(100)
                                md_bg_color: get_color_from_hex("#2196F3")
                                
                            MDFillRoundFlatIconButton:
                                icon: "cup-water"
                                text: "200ml"
                                on_release: app.add_water(200)
                                md_bg_color: get_color_from_hex("#2196F3")
                                
                            MDFillRoundFlatIconButton:
                                icon: "cup-water"
                                text: "300ml"
                                on_release: app.add_water(300)
                                md_bg_color: get_color_from_hex("#2196F3")
                    
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        adaptive_height: True
                        pos_hint: {"center_x": .5}
                        
                        MDFillRoundFlatIconButton:
                            icon: "cup-water"
                            text: "500ml"
                            on_release: app.add_water(500)
                            md_bg_color: get_color_from_hex("#4CAF50")
'''

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
        self.current_intake = 0

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
        user_weight = self.sm.get_screen("create_profile").ids.weight.text
        gender = self.sm.get_screen(
            "create_profile").ids.gender_select.current_active_segment.text

        # Validação da data
        birth_date = birth_date_field.get_date()
        if not birth_date:
            self.show_snackbar("Data de nascimento inválida")
            return

        if not user_name or not user_weight:
            print("Por favor, preencha todos os campos.")
            return

        user = {
            "nome": user_name,
            "peso": float(user_weight),
            "data_nascimento": birth_date,
            "genero": gender,
            "detalhes": []
        }
        print(user)
        # Profile(nome, genero, data_nascimento, peso, detalhes)
        self.user.set_profile(user)
        self.daily_goal = self.user.profile.daily_goal
        if self.user.profile is not None:
            print(f"Perfil criado: {self.user}")
            self.switch_to_tracker()

    def switch_to_create_account(self):
        ...

    def switch_to_tracker(self):
        """Switch to the tracker screen."""
        if not self.user:
            print("Por favor, crie um perfil antes.")
            return

        tracker_screen = self.sm.get_screen("tracker")
        tracker_screen.ids.daily_goal_label.text = f"Meta Diária: {
            Decimal(self.daily_goal).quantize(Decimal('1.'), rounding=ROUND_UP)} mL"
        tracker_screen.ids.progress_label.text = f"Progresso: {self.progress} mL"
        self.water_tracker = WaterTracker(self.user)
        self.sm.current = "tracker"

    def add_water(self, amount):
        """Add water to the progress and update the tracker screen."""
        self.water_tracker.add_water(amount)
        self.current_intake = self.water_tracker.current_intake
        self.progress = self.water_tracker.get_progress()
        tracker_screen = self.sm.get_screen("tracker")
        tracker_screen.ids.progress_label.text = f"Progresso: {self.current_intake} mL"
        tracker_screen.ids.water_add.text = ""
        tracker_screen.ids.progress_bar.value = self.progress

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
        print(f"Peso atualizado: {self.user['weight']} kg, Nova meta: {
              self.daily_goal} ml")
        self.sm.current = "menu"

    def on_gender_select(self, segmentedcontrol, segmentedcontrolitem):
        self.selected_gender = segmentedcontrolitem.text
        self.show_snackbar(f"Gênero selecionado: {self.selected_gender}")

    def show_snackbar(self, msg):
        print(msg)


if __name__ == "__main__":
    HidrataTrackApp().run()
