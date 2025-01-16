from datetime import datetime
from decimal import ROUND_UP, Decimal
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
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
            type: "small"
            size_hint_x: .8
            pos_hint: {"center_x": .5, "center_y": .5}

            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"

            MDTopAppBarTitle:
                text: "HidrataTrack"
                pos_hint: {"center_x": .5}

            MDTopAppBarTrailingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "account-circle-outline"
        
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
                        font_style: "Body"
                        adaptive_height: True
                        
                    MDTextField:
                        id: login
                        mode: "outlined"
                        size_hint_x: None
                        width: "240dp"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        write_tab: False
                        
                        MDTextFieldLeadingIcon:
                            icon: "account"

                        MDTextFieldHintText:
                            text: "Login"
                        MDTextFieldHelperText:
                            text: "Digite seu nome de usuário"
                    
                        
                    MDTextField:
                        id: password
                        mode: "outlined"
                        size_hint_x: None
                        width: "240dp"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        write_tab: False
                        password: True

                        MDTextFieldHintText:
                            text: "Senha"
                        MDTextFieldHelperText:
                            text: "Digite sua senha"
                        
                        MDTextFieldLeadingIcon:
                            icon: "key-variant"
                        
                        
                        
                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#2196F3")
                        on_release: app.authenticate_user()
                        MDButtonText:
                            text: "Entrar"
                        
                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#4CAF50")
                        on_release: app.switch_to_create_account()
                        MDButtonText:
                            text: "Criar Conta"

<CreateProfileScreen>:
    name: "create_profile"
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            type: "small"

            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"

            MDTopAppBarTitle:
                text: "Criar Perfil"
                pos_hint: {"center_x": .5}

            MDTopAppBarTrailingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "account-circle-outline"
            
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
                    
                    MDSegmentedButton:
                        id: gender_select
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_active: app.on_gender_select(*args)
                        
                        MDSegmentedButtonItem:
                            id: male
                            text: "Masculino"
                            
                        MDSegmentedButtonItem:
                            id: female
                            text: "Feminino"

                    MDTextField:
                        id: name
                        mode: "outlined"
                        size_hint_x: None
                        width: "240dp"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        write_tab: False

                        MDTextFieldHintText:
                            text: "Nome"
                        MDTextFieldHelperText:
                            text: "Digite seu nome completo"
                        
                        MDTextFieldTrailingIcon:
                            icon: "account"
                        
                    DateField:
                        id: birth_date
                        size_hint_y: None
                        height: self.minimum_height
                        write_tab: False
                        MDTextFieldHintText:
                            text:  "Data de Nascimento"
                        MDTextFieldHelperText:
                            text: "dd/mm/YYYY"
                            mode: "persistent"
                        MDTextFieldTrailingIcon:
                            icon: "calendar"
                        
                    MDTextField:
                        id: weight
                        mode: "outlined"
                        size_hint_x: None
                        width: "240dp"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        input_filter: "float"
                        write_tab: False

                        MDTextFieldHintText:
                            text: "Peso (kg)"
                        MDTextFieldHelperText:
                            text: "Digite seu peso em quilogramas"
                        MDTextFieldTrailingIcon:
                            icon: "weight-kilogram"
                        
                    MDTextField:
                        id: details
                        multiline: True
                        mode: "outlined"
                        size_hint_x: None
                        width: "240dp"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        write_tab: False
                        max_text_length: 500

                        MDTextFieldHintText:
                            text: "Detalhes adicionais"
                       
                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#4CAF50")
                        on_release: app.create_profile()
                        MDButtonText:
                            text: "Salvar Perfil"

<TrackerScreen>:
    name: "tracker"
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            type: "small"

            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"

            MDTopAppBarTitle:
                text: "Controle Diário"
                pos_hint: {"center_x": .5}

            MDTopAppBarTrailingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "account-circle-outline"
            
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
                        
                    MDLinearProgressIndicator:
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
                                mode: "outlined"
                                size_hint_x: None
                                width: "240dp"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                input_filter: "float"
                                write_tab: False

                                MDTextFieldHintText:
                                    text: "Volume bebido."
                                MDTextFieldHelperText:
                                    text: "Digite o volume em mL"
                            
                            MDIconButton:
                                style: "standard"
                                icon: "water-plus"
                                on_release: app.add_water(float(water_add.text))
                                md_bg_color: get_color_from_hex("#2196F3")
                        
                        MDWidget:

                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_height: True
                            spacing: "10dp"

                            MDButton:
                                style: "filled"
                                on_release: app.add_water(100)
                                md_bg_color: get_color_from_hex("#2196F3")

                                MDButtonIcon:
                                    icon: "cup-water"
                                MDButtonText:
                                    text: "100mL"
                                
                            MDButton:
                                style: "filled"
                                on_release: app.add_water(200)
                                md_bg_color: get_color_from_hex("#2196F3")

                                MDButtonIcon:
                                    icon: "cup-water"
                                MDButtonText:
                                    text: "200mL"
                                
                            MDButton:
                                style: "filled"
                                on_release: app.add_water(300)
                                md_bg_color: get_color_from_hex("#2196F3")

                                MDButtonIcon:
                                    icon: "cup-water"
                                MDButtonText:
                                    text: "300mL"
                    
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        adaptive_height: True
                        pos_hint: {"center_x": .5}
                        
                        MDButton:
                            style: "filled"
                            on_release: app.add_water(500)
                            md_bg_color: get_color_from_hex("#4CAF50")
                                
                            MDButtonIcon:
                                icon: "cup-water"
                            MDButtonText:
                                text: "500mL"
                            
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

from kivymd.utils.set_bars_colors import set_bars_colors

class HidrataTrackApp(MDApp):
    def build(self):
        self.user = None  # Placeholder for user data
        self.daily_goal = 0
        self.progress = 0
        self.current_intake = 0
        self.set_bars_colors()
        self.sm = Builder.load_string(KV)
        return self.sm
    
    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primary_palette,  # status bar color
            self.theme_cls.primary_palette,  # navigation bar color
            "Light",                       # icons color of status bar
        )

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
