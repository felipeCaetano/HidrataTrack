import logging
from services.database import get_session # NoQA
from services.events import EventEmitter # NoQA
from services.water_tracker_service import WaterIntakeService # NoQA

from src.hidratatrack.models.models import Profile
from src.hidratatrack.services.profile_service import get_profile_byname

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,  # Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data/hora
)


class WaterTracker:
    def __init__(self, user=None):
        self.current_profile = None
        self.user = user
        self.current_intake = 0
        self.daily_goal = 0
        self.events = EventEmitter()
        self.session = next(get_session())

    def calculate_daily_goal(self, profile):
        """Calcula a meta diária de água com base no peso do perfil do
        usuário."""
        self.daily_goal = profile.calculate_goal()
        return self.daily_goal

    def add_water(self, amount: float, profile: Profile):
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
        if amount > 1:
            self.events.emit("water_added", f'{amount} mL adicionados!')
        else:
            self.events.emit("water_added", f'{amount} mL adicionado!')

    def reset(self):
        """Reseta o consumo diário de água para zero."""
        self.current_intake = 0
        WaterIntakeService(self.session).reset_daily_intakes(
            self.current_profile)

    def get_progress(self):
        """Retorna o progresso do consumo diário em porcentagem. Retorna 0 se
         a meta diária for zero."""
        if self.daily_goal == 0:
            logging.debug("daile_goel é zer0")
            return 0
        return round((self.current_intake / self.daily_goal) * 100, 2)

    def get_current_intake(self):
        daily_total = WaterIntakeService(self.session).load_daily_intake(
            self.user.profiles[0])
        return daily_total

    def update(self):
        """Recalcula a meta diária de água."""
        self.daily_goal = self.calculate_daily_goal(self.current_profile)

    def set_current_profile(self, profile_name):
        profile_db = get_profile_byname(profile_name)
        if profile_db:
            self.current_profile = profile_db
            self.user.current_profile = self.current_profile
            self.update()
        else:
            self.events.emit("profile-not_found", "Erro ao selecionar perfil")
