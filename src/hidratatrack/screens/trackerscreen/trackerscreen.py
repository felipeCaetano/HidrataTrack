from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from services.events import EventEmitter
from services.water_tracker_service import WaterIntakeService
from utils.snackbar_utils import show_snackbar


class TrackerScreen(MDScreen):
    user_definide = 350
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.events = EventEmitter()
        # Registra handlers para os eventos
        self.events.on("water_warning", self.handle_warning)
        self.events.on("water_added", self.handle_water_added)
        
    
    def handle_warning(self, message: str):
        """Handler para avisos relacionados ao consumo de água."""
        # show_snackbar(message)
    
    def handle_water_added(self, volume: float):
        """Handler para quando água é adicionada."""
        # Atualiza a UI conforme necessário
        pass

    def add_water(self, amount, user, session):
        try:
            if not user:
                return
            WaterIntakeService(session).save_water_intake(user, amount)

            # Atualiza progresso
            daily_total = WaterIntakeService(session).load_daily_intake(self.user)
            self.update_tracker_progress(daily_total)
        
        except ValueError as e:
            show_snackbar(str(e))

    def update_tracker_progress(self, daily_total):
        """Atualiza os componentes da interface com os dados mais recentes."""
        # tracker_screen = self.root.get_screen("tracker")
        self.progress = self.water_tracker.get_progress()
        self.ids.progress_bar.value = self.progress
        self.ids.water_add.text = ""
        self.ids.progress_label.text = f"Progresso: {daily_total} mL"
        self.ids.bar_indicator.text = f"{self.progress} %"

    def menu_open(self):

        menu_items = [
            {
            "text": f"Perfil {i}",
                "on_release": lambda x=f"Perfil {i}": self.menu_callback(x),
            } for i in range(5)
        ]
        MDDropdownMenu(
            caller=self.ids.button,
            items=menu_items,
            position='bottom',
            width=dp(160)
        ).open()

    def menu_callback(self, text_item):
        app = MDApp.get_running_app()
        print(app.user.profiles)
        print(text_item)
        self.ids.profile_button.text = text_item