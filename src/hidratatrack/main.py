from kivy.uix.filechooser import string_types
from datetime import date
from decimal import ROUND_UP, Decimal

from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.utils.set_bars_colors import set_bars_colors
from sqlalchemy import func
from models.models import Profile, User, WaterIntake, session
from models.water_tracker import WaterTracker
from screens.createuserscreen.createuser import CreateUserScreen
from screens.login.loginscreen import LoginScreen
from screens.profile.createprofilescreen import CreateProfileScreen
from screens.trackerscreen.trackerscreen import TrackerScreen


class MainApp(MDApp):

    def __init__(self, *args):
        super(MainApp, self).__init__(*args)
        self.user = None
        self.daily_goal = 0
        self.progress = 0
        self.current_intake = 0
        self.water_tracker = None
        self.set_bars_colors()

    def build(self):
        self.title = "HidrataTrack"

    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primary_palette,  # status bar color
            self.theme_cls.primary_palette,  # navigation bar color
            "Light",  # icons color of status bar
        )

    def save_user(self, user: User):
        """Salva um usuário no banco de dados."""
        existing_user = session.query(User).filter_by(login=user.login).first()
        if existing_user:
            self.show_snackbar(f"Usuário {user.login} já existe.")
            return existing_user
        # new_user = User(login=user.login, email=user.email,
        #                 password=user.password)
        session.add(user)
        session.commit()
        self.show_snackbar(f"Usuário {user.login} salvo com sucesso.")
        return user

    def save_profile(self, profile: Profile):
        existing_profile = session.query(
            Profile).filter_by(name=profile.name).first()
        if existing_profile:
            self.show_snackbar(f"Perfil {profile.name} já existe.")
            return existing_profile
        self.user.profiles = profile
        session.add(profile)
        session.commit()
        self.show_snackbar(f"Perfil {profile.name} salvo com sucesso.")
        return profile

    def show_date_picker(self, focus):
        if not focus:
            return

        self.date_dialog = MDDockedDatePicker(
            theme_bg_color="Custom",  # Cor principal do calendário
            scrim_color=(1, 1, 1, 0),  # Cor do texto dos botões
            theme_text_color="Secondary",  # Cor da data atual
            supporting_text="Selecione a data",
            year='1952'
        )
        self.date_dialog.bind(
            on_ok=self.on_ok,
            on_select_day=self.on_select_day,
            on_cancel=self.on_cancel_date,
        )
        self.date_dialog.open()

    def on_ok(self, instance_date_picker):
        date = instance_date_picker.get_date()[0]
        birth_date_field = self.root.get_screen(
            "create_profile").ids.birth_date
        self.set_date_field(instance_date_picker, date, birth_date_field)

    def set_date_field(self, instance_date_picker, date, birth_date_field):
        birth_date_field.text = date.strftime("%d/%m/%Y")
        instance_date_picker.dismiss()

    def on_select_day(self, instance, value):
        """Esta função será chamada quando uma data for selecionada"""
        birth_date_field = self.root.get_screen(
            "create_profile").ids.birth_date
        data = date(instance.sel_year, instance.sel_month, value)
        self.set_date_field(instance, data, birth_date_field)

    def on_cancel_date(self, instance):
        """Esta função será chamada quando o usuário cancelar a seleção"""
        instance.dismiss()

    def switch_to_create_account(self):
        self.root.current = "createuser"

    def switch_to_login(self):
        self.root.current = "login"

    def switch_to_tracker(self):
        """Switch to the tracker screen."""
        if not self.user:
            print("Por favor, crie um perfil antes.")
            return
        
        self.water_tracker = WaterTracker()
        tracker_screen = self.root.get_screen("tracker")
        tracker_screen.ids.daily_goal_label.text = f"Meta Diária: {
            Decimal(self.daily_goal).quantize(Decimal('1.'), rounding=ROUND_UP)} mL"
        tracker_screen.ids.progress_label.text = f"Progresso: {
            Decimal(
                self.water_tracker.current_intake).quantize(
                    Decimal('1.'), rounding=ROUND_UP)} mL"
        self.progress = self.water_tracker.get_progress()
        tracker_screen.ids.progress_bar.value = self.progress
        tracker_screen.ids.bar_indicator.text = f"{self.progress} %"
        self.root.current = "tracker"

    def add_water(self, amount):
        """Add water to the progress and update the tracker screen."""
        if not hasattr(self, "water_tracker"):
            self.water_tracker = WaterTracker(self.user)
        if amount:
            try:
                self.water_tracker.add_water(float(amount))
            except ValueError:
                self.show_snackbar("Atenção! O valor deve ser um número válido")
        else:
            self.show_snackbar("Atenção! O campo não pode ser vazio!")
        # self.current_intake = self.water_tracker.current_intake
        # self.progress = self.water_tracker.get_progress()
        # tracker_screen = self.root.get_screen("tracker")
        # tracker_screen.ids.progress_label.text = f"Progresso: {
        #     self.current_intake} mL"
        # tracker_screen.ids.water_add.text = ""
        # tracker_screen.ids.progress_bar.value = self.progress
        if not self.user or not self.user.profiles:
            print("Usuário ou perfil não encontrado.")
            return

        self.save_water_intake(self.user, amount)
        daily_total = self.load_daily_intake(self.user)
        self.current_intake = self.water_tracker.current_intake
        self.progress = self.water_tracker.get_progress()
        tracker_screen = self.root.get_screen("tracker")
        tracker_screen.ids.water_add.text = ""
        tracker_screen.ids.progress_bar.value = self.progress
        tracker_screen.ids.progress_label.text = f"Progresso: {daily_total} ml"
        tracker_screen.ids.bar_indicator.text = f"{self.progress} %"
        print(f"{amount} ml adicionados. Consumo diário total: {daily_total} ml.")

    def switch_to_profile(self, user):
        """Switch to the profile screen."""
        self.user = user
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
            MDSnackbarText(
                text=msg,
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()

    def show_water_history(self):
        """Exibe o histórico de consumo de água."""
        if not self.current_user:
            print("Usuário não encontrado.")
            return

        history = self.load_water_history(self.current_user)
        for entry in history:
            print(f"Data: {entry.date}, Quantidade: {entry.amount} ml")

    def save_water_intake(self, user, amount):
        """Registra o consumo de água para o usuário."""
        if not user:
            print("Usuário não encontrado para registrar o consumo.")
            return

        intake = WaterIntake(user_id=user.id, date=date.today(), amount=amount)
        session.add(intake)
        session.commit()
        print(f"{amount} ml de água registrados para o usuário {user.login}.")
        return intake
    
    def load_daily_intake(self, user):
        """Carrega o consumo total de água do dia para o usuário."""
        if not user:
            print("Usuário não encontrado para carregar o consumo.")
            return 0

        daily_total = session.query(func.sum(WaterIntake.amount)).filter_by(
            user_id=user.id).scalar()
        # total = sum(intake.amount for intake in daily_total)
        print(f"Consumo total de hoje: {daily_total} ml.")
        return daily_total
    
    def load_water_history(self, user):
        """Carrega o histórico completo de consumo de água do usuário."""
        if not user:
            print("Usuário não encontrado para carregar o histórico.")
            return []

        history = session.query(WaterIntake).filter_by(user_id=user.id).all()
        print(f"Histórico carregado para o usuário {user.login}.")
        return history
    

if __name__ == "__main__":
    Window.size = (317, 715)  # não use para android ou ios
    MainApp().run()
