import logging
from services.database import get_session  # NoQA
from services.events import EventEmitter  # NoQA
from services.water_tracker_service import WaterIntakeService  # NoQA

from models.models import Profile
from services.profile_service import get_profile_byname

from src.hidratatrack.services.profile_service import update_bottle_volume

logging.basicConfig(
    level=logging.INFO,  # Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato da data/hora
)


class WaterTracker:
    def __init__(self, user=None):
        self.user = user
        self.session = get_session
        self.current_profile = self.user.profiles[0]
        self.current_intake = self.get_current_intake()
        self.daily_goal = self.calculate_daily_goal(self.current_profile)
        self.events = EventEmitter()

    def calculate_daily_goal(self, profile):
        """Calcula a meta diária de água com base no peso do perfil do
        usuário."""
        self.daily_goal = profile.calculate_goal()
        return self.daily_goal

    def add_water(self, amount: float, profile: Profile):
        """Adiciona um volume de água ao consumo diário."""
        with self.session() as session:
            if amount <= 0:
                self.events.emit(
                    "water_warning",
                    "ALERTA! Quantidade de água deve ser maior que zero.",
                )
                return

            self.current_intake += amount
            if self.current_intake > self.daily_goal:
                self.current_intake = self.daily_goal
                self.events.emit(
                    "water_warning", "ALERTA! Você ultrapassou o consumo diário!"
                )
            WaterIntakeService(session).save_water_intake(profile, amount)
            if amount > 1:
                self.events.emit("water_added", f"{amount} mL adicionados!")
            else:
                self.events.emit("water_added", f"{amount} mL adicionado!")

    def reset(self):
        """Reseta o consumo diário de água para zero."""
        with self.session() as session:
            self.current_intake = 0
            self.get_progress()
            WaterIntakeService(session).reset_daily_intakes(self.current_profile)

    def get_progress(self) -> float:
        """Retorna o progresso do consumo diário em porcentagem.
        Returns:
            float: O progresso em porcentagem (0 a 100).
            Retorna 0 se a meta diária for zero.
        """
        if not self.daily_goal:
            logging.debug("Meta diária é zero.")
            return 0.0
        progress = (self.current_intake / self.daily_goal) * 100
        return round(progress, 2)

    def get_current_intake(self):
        with self.session() as session:
            try:
                daily_total = WaterIntakeService(session).load_daily_intake(
                    self.current_profile
                )
                return daily_total
            except RuntimeError as error:
                self.events.emit("database-error", str(error))
                return 0

    def update(self):
        """Recalcula a meta diária de água."""
        self.daily_goal = self.calculate_daily_goal(self.current_profile)

    def set_current_profile(self, profile_name):
        with self.session() as session:
            profile_db = get_profile_byname(profile_name, session)
            if not profile_db:
                self.events.emit("profile-not_found", "Erro ao selecionar perfil")
                return
            self.current_profile = profile_db
            self.user.current_profile = self.current_profile
            self.update()

    def personalize_bottle_volume(self, user_defined):
        with self.session() as session:
            update_bottle_volume(session, self.current_profile.id, user_defined)
