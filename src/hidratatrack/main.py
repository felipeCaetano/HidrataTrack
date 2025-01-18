from datetime import date, datetime
from decimal import ROUND_UP, Decimal

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedbutton import MDSegmentedButton
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.utils.set_bars_colors import set_bars_colors

from user import User
from water_tracker import WaterTracker

# KivyMD Builder String for Layout
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import DateField datefield

ScreenManager:
    transition: FadeTransition()
    LoginScreen:
    TrackerScreen:
    CreateProfileScreen:
    SettingsScreen:
#     
# 
<LoginScreen>:
    name: "login"
# 
    MDBoxLayout:
        orientation: "vertical"
# 
        MDFloatLayout:
            MDCard:
                size_hint: None, None
                size: "300dp", "400dp"
                pos_hint: {"center_x": .5, "center_y": .5}
                padding: "20dp"
                spacing: "20dp"
                elevation: 3
                adaptive_height: True
# 
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "20dp"
                    adaptive_height: True

                    MDAnchorLayout:
                        size_hint: 1, None
                        height: "120dp" 
                        padding: "10dp"
                        
                        FitImage:
                            source: "hidratatrack.png"
                            size_hint: None, None
                            size: "120dp", "120dp"
                            pos_hint: {"center_x": .5, "center_y": .5}

                    MDLabel:
                        text: "Bem-vindo"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "Display"
                        role: "small"
                        adaptive_height: True
# 
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
# 
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
# 
                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#2196F3")
                        on_release: app.authenticate_user()
                        MDButtonText:
                            text: "Entrar"
# 
                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#4CAF50")
                        on_release: app.switch_to_create_account()
                        MDButtonText:
                            text: "Criar Conta"
# 
<CreateProfileScreen>:
    name: "create_profile"

    MDBoxLayout:
        orientation: "vertical"
# 
        MDTopAppBar:
            type: "small"
# 
            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"

            MDTopAppBarTitle:
                text: "Criar Perfil"
                pos_hint: {"center_x": .5}
# 
#             MDTopAppBarTrailingButtonContainer:
# 
#                 MDActionTopAppBarButton:
#                     icon: "account-circle-outline"
# 
        MDFloatLayout:
            MDCard:
                size_hint: None, None
                size: "500dp", "520dp"
                pos_hint: {"center_x": .5, "center_y": .5}
                padding: "20dp"
                spacing: "20dp"
                elevation: 3
# 
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "20dp"

                    MDLabel:
                        text: "Informações Pessoais"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "Title"
# 
                    MDSegmentedButton:
                        id: gender_select
                        type: "normal"
                        adaptive_height: True
                        radius: 45
                        pos_hint: {"center_x": .5, "center_y": .5}

                        MDSegmentedButtonItem:
                            id: male
                            # on_active: app.on_gender_select(*args)
                            MDSegmentButtonIcon:
                                icon: ""
                            MDSegmentButtonLabel:
                                text: "Masculino"

                        MDSegmentedButtonItem:
                            id: female
                            MDSegmentButtonLabel:
                                text: "Feminino"
# 
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
# 
                    MDTextField:
                        id: birth_date
                        mode: "outlined"
                        size_hint_x: None
                        width: "240dp"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        write_tab: False
                        readonly: True  # Importante para evitar edição manual
                        on_focus: app.show_date_picker(self.focus)  # Chama 

                        MDTextFieldHintText:
                            text: "Data de Nascimento"
                        MDTextFieldHelperText:
                            text: "Clique para selecionar a data"
                        MDTextFieldTrailingIcon:
                            icon: "calendar"
# 
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
                        mode: "outlined"
                        size_hint_x: None
                        width: "240dp"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        write_tab: False
                        max_text_length: 500

                        MDTextFieldHintText:
                            text: "Detalhes adicionais"
                        MDTextFieldHelperText:
                            text: "Digite informações sobre sua saúde"

                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        md_bg_color: get_color_from_hex("#4CAF50")
                        on_release: app.create_profile()
                        MDButtonText:
                            text: "Salvar Perfil"
# 
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
# 
#             MDTopAppBarTrailingButtonContainer:
# 
#                 MDActionTopAppBarButton:
#                     icon: "account-circle-outline"
# 
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
                        font_style: "Title"
                        role: "large"
# 
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
# 
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
# 
                                MDTextFieldHintText:
                                    text: "Volume bebido."
                                MDTextFieldHelperText:
                                    text: "Digite o volume em mL"
# 
                            MDIconButton:
                                style: "standard"
                                icon: "water-plus"
                                on_release: app.add_water(water_add.text)
                                md_bg_color: get_color_from_hex("#2196F3")

                        MDWidget:
# 
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
# 
                            MDButton:
                                style: "filled"
                                on_release: app.add_water(300)
                                md_bg_color: get_color_from_hex("#2196F3")

                                MDButtonIcon:
                                    icon: "cup-water"
                                MDButtonText:
                                    text: "300mL"
# 
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
            "Light",  # icons color of status bar
        )

    def authenticate_user(self):
        login = self.sm.get_screen("login").ids.login.text
        password = self.sm.get_screen("login").ids.password.text

        # Placeholder for authentication logic
        if login == "test" and password == "1234":
            self.user = User(login, password)
            if self.user.profile is None:
                self.switch_to_profile()
            else:
                self.switch_to_tracker()
        else:
            self.show_snackbar("Login ou senha inválidos.")

    def create_profile(self):
        """Create a user profile and calculate the daily water goal."""
        self.sm.get_screen(
            "create_profile").ids.gender_select.adjust_segment_radius(15)
        user_name = self.sm.get_screen("create_profile").ids.name.text
        birth_date_field = self.sm.get_screen("create_profile").ids.birth_date
        user_weight = self.sm.get_screen("create_profile").ids.weight.text
        gender_selector: MDSegmentedButton = self.sm.get_screen(
            "create_profile").ids.gender_select
        try:
            gender = gender_selector.get_marked_items()[0]._label.text
        except IndexError:
            force_selected = gender_selector.get_items()[0]
            gender_selector.mark_item(force_selected)
            gender = gender_selector.get_marked_items()[0]._label.text

        # Validação da data
        birth_date = birth_date_field.text
        if not birth_date:
            self.show_snackbar("Data de nascimento inválida")
            return
        else:
            date_obj = datetime.strptime(birth_date, '%d/%m/%Y')

        if not all([user_name, user_weight, gender, date_obj]):
            self.show_snackbar("Por favor, preencha todos os campos.")
            return

        user = {
            "nome": user_name,
            "peso": float(user_weight),
            "data_nascimento": date_obj,
            "genero": gender,
            "detalhes": []
        }
        # Profile(nome, genero, data_nascimento, peso, detalhes)
        self.user.set_profile(user)
        self.daily_goal = self.user.profile.daily_goal
        if self.user.profile is not None:
            print(f"Perfil criado: {self.user}")
            self.switch_to_tracker()

    def show_date_picker(self, focus):
        if not focus:
            return

        self.date_dialog = MDDockedDatePicker(
            theme_bg_color="Custom",  # Cor principal do calendário
            scrim_color=(1, 1, 1, 0),  # Cor do texto dos botões
            theme_text_color="Secondary",  # Cor da data atual
            supporting_text="Selecione a data"
        )
        self.date_dialog.bind(
            on_ok=self.on_ok,
            on_select_day=self.on_select_day,
            on_cancel=self.on_cancel_date
        )
        self.date_dialog.open()

    def on_ok(self, instance_date_picker):
        data = instance_date_picker.get_date()[0]
        birth_date_field = self.root.get_screen(
            'create_profile').ids.birth_date
        self.set_date_field(instance_date_picker, data, birth_date_field)

    def set_date_field(self, instance_date_picker, data, birth_date_field):
        birth_date_field.text = data.strftime('%d/%m/%Y')
        instance_date_picker.dismiss()

    def on_select_day(self, instance, value):
        """
        Esta função será chamada quando uma data for selecionada
        """
        # pegar o mes e o ano para assim gerar uma data
        birth_date_field = self.root.get_screen(
            'create_profile').ids.birth_date
        data = date(instance.sel_year, instance.sel_month, value)
        self.set_date_field(instance, data, birth_date_field)

    def on_cancel_date(self, instance):
        """
        Esta função será chamada quando o usuário cancelar a seleção
        """
        instance.dismiss()

    def switch_to_create_account(self):
        ...

    def switch_to_tracker(self):
        """Switch to the tracker screen."""
        if not self.user:
            print("Por favor, crie um perfil antes.")
            return

        tracker_screen = self.sm.get_screen("tracker")
        tracker_screen.ids.daily_goal_label.text = f"Meta Diária: {
        Decimal(self.daily_goal).quantize(Decimal('1.'), rounding=ROUND_UP)}mL"
        tracker_screen.ids.progress_label.text = f"Progresso: {self.progress}mL"
        self.water_tracker = WaterTracker(self.user)
        self.sm.current = "tracker"

    def add_water(self, amount):
        """Add water to the progress and update the tracker screen."""
        if not getattr(self, 'water_tracker'):
            self.water_tracker = WaterTracker(self.user)
        if amount is not None:
            self.water_tracker.add_water(float(amount))
        else:
            return "O campo está vazio!"
        self.current_intake = self.water_tracker.current_intake
        self.progress = self.water_tracker.get_progress()
        tracker_screen = self.sm.get_screen("tracker")
        tracker_screen.ids.progress_label.text = f"Progresso: {
        self.current_intake} mL"
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
        self.sm.current = "menu"

    # def on_gender_select(self, segmentedcontrol, segmentedcontrolitem):
    #     self.selected_gender = segmentedcontrolitem.text
    #     self.show_snackbar(f"Gênero selecionado: {self.selected_gender}")

    def show_snackbar(self, msg):
        MDSnackbar(
            MDSnackbarText(text=msg, ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()


if __name__ == "__main__":
    HidrataTrackApp().run()
