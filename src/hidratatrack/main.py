from datetime import date, datetime
from decimal import ROUND_UP, Decimal

from kivy.core.window import Window
from kivymd.uix.segmentedbutton import MDSegmentedButton
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.uix.pickers import MDDockedDatePicker

from kivy.clock import Clock

from models.user import User
from models.water_tracker import WaterTracker
from screens.login.loginscreen import LoginScreen
from screens.profile.createprofilescreen import CreateProfileScreen
from screens.trackerscreen.trackerscreen import TrackerScreen


#Screens
class SettingsScreen(MDScreen):
    pass


class MainApp(MDApp):

    # def __init__(self, *args):
        # super(HidrataTrackApp, self).__init__(*args)
        # self.user = None  # Placeholder for user data
        # self.daily_goal = 0
        # self.progress = 0
        # self.current_intake = 0
        # self.set_bars_colors()

    def build(self):
        self.user = None  # Placeholder for user data
        self.daily_goal = 0
        self.progress = 0
        self.current_intake = 0
        self.set_bars_colors()
        self.title = 'HidrataTrack'
        # Builder.load_file('main.kv')
        # sm = ScreenManager()
        # sm.add_widget(LoginScreen(name="login"))
        # return sm 
        # return self.sm
    
    # def on_start(self):
    #     self.root.current = "login_screen"

    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primary_palette,  # status bar color
            self.theme_cls.primary_palette,  # navigation bar color
            "Light",  # icons color of status bar
        )

    def authenticate_user(self):
        login = self.root.get_screen("login").ids.login.text
        password = self.root.get_screen("login").ids.password.text

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
        self.root.get_screen(
            "create_profile").ids.gender_select.adjust_segment_radius(15)
        user_name = self.root.get_screen("create_profile").ids.name.text
        birth_date_field = self.root.get_screen("create_profile").ids.birth_date
        user_weight = self.root.get_screen("create_profile").ids.weight.text
        try:
            gender_selector: MDSegmentedButton = self.root.get_screen(
                "create_profile").ids.gender_select
            gender = gender_selector.get_marked_items()[0]._label.text
        except IndexError:
            force_selected = gender_selector.get_items()[0]
            gender_selector.mark_item(force_selected)
            gender = gender_selector.get_marked_items()[0]._label.text

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
        date = instance_date_picker.get_date()[0]
        birth_date_field = self.root.get_screen(
            'create_profile').ids.birth_date
        self.set_date_field(instance_date_picker, date, birth_date_field)

    def set_date_field(self, instance_date_picker, date, birth_date_field):
        birth_date_field.text = date.strftime('%d/%m/%Y')
        instance_date_picker.dismiss()

    def on_select_day(self, instance, value):
        """
        Esta função será chamada quando uma data for selecionada
        """
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

        tracker_screen = self.root.get_screen("tracker")
        tracker_screen.ids.daily_goal_label.text = f"Meta Diária: {
        Decimal(self.daily_goal).quantize(Decimal('1.'), rounding=ROUND_UP)} mL"
        tracker_screen.ids.progress_label.text = f"Progresso: {self.progress} mL"
        self.water_tracker = WaterTracker(self.user)
        self.root.current = "tracker"

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
        tracker_screen = self.root.get_screen("tracker")
        tracker_screen.ids.progress_label.text = f"Progresso: {self.current_intake} mL"
        tracker_screen.ids.water_add.text = ""
        tracker_screen.ids.progress_bar.value = self.progress

    def switch_to_profile(self):
        """Switch to the profile screen."""
        self.root.current = "create_profile"

    def update_weight(self):
        """Update the user's weight and recalculate the daily goal."""
        new_weight = self.root.get_screen("settings").ids.new_weight.text

        if not new_weight or not self.user:
            print("Peso inválido ou perfil não criado.")
            return

        self.user["weight"] = float(new_weight)
        self.daily_goal = (float(new_weight) / 20) * 1000
        self.root.current = "menu"

    def on_gender_select(self, segmentedcontrol, segmentedcontrolitem):
        self.selected_gender = segmentedcontrolitem.text
        self.show_snackbar(f"Gênero selecionado: {self.selected_gender}")

    def show_snackbar(self, msg):
        MDSnackbar(
            MDSnackbarText(text=msg, ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()


if __name__ == "__main__":
    Window.size = (317, 715) # não use para android ou ios
    MainApp().run()
