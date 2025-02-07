import logging

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from services.events import EventEmitter

from utils.snackbar_utils import show_snackbar


from src.hidratatrack.services.water_tracker import WaterTracker



class TrackerScreen(MDScreen):
    user_definide = 350
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.water_tracker = None
        self.menu = None
        self.menu_items = None
        self.app = MDApp.get_running_app()
        self.events = EventEmitter()
        # Registra handlers para os eventos
        self.events.on("water_warning", self.handle_warning)
        self.events.on("water_added", self.handle_water_added)

    def on_enter(self, *args):
        self.menu_items = self.generate_menu_items()
        self.water_tracker = WaterTracker(self.app.user)
        
    def generate_menu_items(self):
        menu_items = []
        for profile in self.app.user.profiles:
            menu_items.append({
                "text": f"{profile.name}",
                "on_release": lambda x=f"{profile.name}": self.menu_callback(x),
                })
        return menu_items

    
    def handle_warning(self, message: str):
        """Handler para avisos relacionados ao consumo de água."""
        # show_snackbar(message)
    
    def handle_water_added(self, message: str):
        """Handler para quando água é adicionada."""
        # Atualiza a UI conforme necessário
        show_snackbar(message)

    def add_water(self, amount):
        user = self.app.user
        try:
            amount = float(amount)
            if not user:
                return
            self.water_tracker.add_water(amount, self.app.user.profiles)
            # Atualiza progresso
            daily_total = self.water_tracker.get_current_intake()
            self.update_tracker_progress(daily_total)
        
        except ValueError as e:
            show_snackbar(str(e))

    def update_tracker_progress(self, daily_total):
        """Atualiza os componentes da interface com os dados mais recentes."""
        # tracker_screen = self.root.get_screen("tracker")
        self.progress = self.water_tracker.get_progress()
        logging.debug(f'{self.progress=}')
        self.ids.progress_bar.value = self.progress
        self.ids.water_add.text = ""
        self.ids.progress_label.text = f"Progresso: {daily_total} mL"
        self.ids.bar_indicator.text = f"{self.progress} %"

    def menu_open(self):
        self.menu = MDDropdownMenu(
            caller=self.ids.button,
            items=self.menu_items,
            position='bottom',
            width=dp(160)
        )
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.ids.profile_button.text = text_item