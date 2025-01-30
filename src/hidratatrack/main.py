from datetime import date
from decimal import ROUND_UP, Decimal

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.utils.set_bars_colors import set_bars_colors
from sqlalchemy import func

from models.models import Profile, User, WaterIntake, session
from services.water_tracker import WaterTracker
from screens.createuserscreen.createuser import CreateUserScreen    # NoQA
from screens.login.loginscreen import LoginScreen   # NoQA
from screens.profile.createprofilescreen import CreateProfileScreen # NoQA
from screens.trackerscreen.trackerscreen import TrackerScreen   # NoQA
from services.water_tracker_service import WaterIntakeService
from utils.snackbar_utils import show_snackbar   # NoQA


class MainApp(MDApp):

    def __init__(self):
        super(MainApp, self).__init__()
        self.date_dialog = None
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
            show_snackbar(f"Usuário {user.login} já existe.")
            return existing_user
        session.add(user)
        session.commit()
        show_snackbar(f"Usuário {user.login} salvo com sucesso.")
        return user

    def save_profile(self, profile: Profile):
        existing_profile = session.query(
            Profile).filter_by(name=profile.name).first()
        if existing_profile:
            show_snackbar(f"Perfil {profile.name} já existe.")
            return existing_profile
        self.user.profiles = profile
        session.add(profile)
        session.commit()
        show_snackbar(f"Perfil {profile.name} salvo com sucesso.")
        return profile

    def show_date_picker(self, focus):
        if not focus:
            return

        self.date_dialog = MDDockedDatePicker(
            theme_bg_color="Custom",  # Cor principal do calendário
            scrim_color=(1, 1, 1, 0),  # Cor do texto dos botões
            theme_text_color="Secondary",  # Cor da data atual
            supporting_text="Selecione a data",
            sel_year=1952
        )
        self.date_dialog.bind(
            on_ok=self.on_ok,
            on_select_day=self.on_select_day,
            on_cancel=self.on_cancel_date,
        )
        self.date_dialog.open()

    def on_ok(self, instance_date_picker):
        pick_date = instance_date_picker.get_date()[0]
        birth_date_field = self.root.get_screen(
            "create_profile").ids.birth_date
        self.set_date_field(instance_date_picker, birth_date_field, pick_date)

    def set_date_field(
            self, instance_date_picker, birth_date_field, pick_date
    ):
        birth_date_field.text = pick_date.strftime("%d/%m/%Y")
        instance_date_picker.dismiss()

    def on_select_day(self, instance, value):
        """Esta função será chamada quando uma data for selecionada"""
        birth_date_field = self.root.get_screen(
            "create_profile").ids.birth_date
        data = date(instance.sel_year, instance.sel_month, value)
        self.set_date_field(instance, birth_date_field, data)

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
            show_snackbar("Por favor, crie um perfil antes.")
            return

        self.water_tracker = WaterTracker()
        tracker_screen = self.root.get_screen("tracker")
        tracker_screen.ids.daily_goal_label.text = f"Meta Diária: {
            Decimal(self.daily_goal).quantize(
                Decimal('1.'), rounding=ROUND_UP)} mL"
        tracker_screen.ids.progress_label.text = f"Progresso: {
            Decimal(self.water_tracker.current_intake).quantize(
                Decimal('1.'), rounding=ROUND_UP)} mL"
        self.progress = self.water_tracker.get_progress()
        tracker_screen.ids.progress_bar.value = self.progress
        tracker_screen.ids.bar_indicator.text = f"{self.progress} %"
        self.root.current = "tracker"

    def add_water(self, amount):
        """Add water to the progress and update the tracker screen."""
        try:
            if not self.water_tracker:
                self.water_tracker = WaterTracker()
            # Valida e salva consumo
            self.water_tracker.add_water(amount)
            WaterIntakeService(session).save_water_intake(self.user, amount)

            # Atualiza progresso
            daily_total = WaterIntakeService(session).load_daily_intake(self.user)
            self.update_tracker_progress(daily_total)

        except ValueError as e:
            show_snackbar(str(e))

    def update_tracker_progress(self, daily_total):
        """Atualiza os componentes da interface com os dados mais recentes."""
        tracker_screen = self.root.get_screen("tracker")
        self.progress = self.water_tracker.get_progress()
        tracker_screen.ids.progress_bar.value = self.progress
        tracker_screen.ids.water_add.text = ""
        tracker_screen.ids.progress_label.text = f"Progresso: {daily_total} mL"
        tracker_screen.ids.bar_indicator.text = f"{self.progress} %"

    def switch_to_profile(self, user):
        """Switch to the profile screen."""
        self.user = user
        self.root.current = "create_profile"

    def update_weight(self):
        """Update the user's weight and recalculate the daily goal."""
        new_weight = self.root.get_screen("settings").ids.new_weight.text

        if not new_weight or not self.user:
            show_snackbar("Peso inválido ou perfil não criado.")
            return

        self.user["weight"] = float(new_weight)
        self.daily_goal = (float(new_weight) / 20) * 1000
        self.root.current = "menu"

    def show_water_history(self):
        """Exibe o histórico de consumo de água."""
        if not self.user:
            show_snackbar("Usuário não encontrado.")
            return

        history = self.load_water_history(self.user)
        for entry in history:
            show_snackbar(
                f"Data: {entry.date}, Quantidade: {entry.amount} ml")

    def save_water_intake(self, user, amount):
        """Registra o consumo de água para o usuário."""
        if not user:
            show_snackbar(
                "Usuário não encontrado para registrar o consumo.")
            return

        intake = WaterIntake(user_id=user.id, date=date.today(), amount=amount)
        session.add(intake)
        session.commit()
        show_snackbar(
            f"{amount} ml de água registrados para o usuário {user.login}.")
        return intake

    def load_daily_intake(self, user):
        """Carrega o consumo total de água do dia para o usuário."""
        if not user:
            print("Usuário não encontrado para carregar o consumo.")
            return 0

        daily_total = session.query(func.sum(WaterIntake.amount)).filter_by(
            user_id=user.id).scalar()
        return daily_total or 0

    def load_water_history(self, user):
        """Carrega o histórico completo de consumo de água do usuário."""
        if not user:
            show_snackbar(
                "Usuário não encontrado para carregar o histórico.")
            return []

        history = session.query(WaterIntake).filter_by(user_id=user.id).all()
        show_snackbar(f"Histórico carregado para o usuário {user.login}.")
        return history


if __name__ == "__main__":
    Window.size = (317, 715)  # não use para android ou ios
    MainApp().run()
