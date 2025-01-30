from kivymd.uix.screen import MDScreen

from services.events import EventEmitter
from utils.snackbar_utils import show_snackbar


class TrackerScreen(MDScreen):
    user_definide = 350
    def __init__(self):
        super().__init__()
        self.events = EventEmitter()
        # Registra handlers para os eventos
        self.events.on("water_warning", self.handle_warning)
        self.events.on("water_added", self.handle_water_added)
    
    def handle_warning(self, message: str):
        """Handler para avisos relacionados ao consumo de água."""
        show_snackbar(message)
    
    def handle_water_added(self, volume: float):
        """Handler para quando água é adicionada."""
        # Atualiza a UI conforme necessário
        pass



