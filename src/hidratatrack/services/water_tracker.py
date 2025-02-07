import logging
from services.database import get_session
from services.events import EventEmitter
from services.water_tracker_service import WaterIntakeService

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,  # Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data/hora
)


class WaterTracker:
    def __init__(self, user=None):
        self.user = user
        self.current_intake = 0
        self.daily_goal = self.calculate_daily_goal()
        self.events = EventEmitter()
        self.session = next(get_session())

        if self.user and self.user.profiles:
            self.daily_goal = self.calculate_daily_goal()

    def calculate_daily_goal(self):
        """Calcula a meta diária de água com base no peso do perfil do
        usuário.
        Retorna 0 se o usuário não tiver um perfil."""
        if self.user and self.user.profiles:
            profile = self.user.profiles[0]
            return profile.calculate_goal()
        logging.info("Retornando zero")
        return 0

    def add_water(self, amount: float, profile):
        """Adiciona um volume de água ao consumo diário."""
        if amount <= 0:
            self.events.emit(
                "water_warning",
                "ALERTA! Quantidade de água deve ser maior que zero.")
            return

        self.current_intake += amount
        if self.current_intake > self.daily_goal:
            self.current_intake = self.daily_goal
            self.events.emit("water_warning",
                             "ALERTA! Você ultrapassou o consumo diário!")
        WaterIntakeService(self.session).save_water_intake(profile, amount)
        self.events.emit("water_added", amount)

    def reset(self):
        """Reseta o consumo diário de água para zero."""
        self.current_intake = 0

    def get_progress(self):
        """Retorna o progresso do consumo diário em porcentagem. Retorna 0 se
         a meta diária for zero."""
        if self.daily_goal == 0:
            logging.debug("daile_goel é zer")
            return 0
        return (self.current_intake / self.daily_goal) * 100

    def get_current_intake(self):
        daily_total = WaterIntakeService(self.session).load_daily_intake(
            self.user.profiles[0])

    def update(self):
        """Recalcula a meta diária de água."""
        self.daily_goal = self.calculate_daily_goal()
