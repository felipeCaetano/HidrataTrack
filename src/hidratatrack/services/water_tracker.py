
from services.events import EventEmitter


class WaterTracker:
    def __init__(self, user=None):
        self.user = user
        self.current_intake = 0
        self.daily_goal = self.calculate_daily_goal()
        self.events = EventEmitter()

        if self.user and self.user.profiles:
            self.daily_goal = self.calculate_daily_goal()

    def calculate_daily_goal(self):
        """Calcula a meta diária de água com base no peso do perfil do
        usuário.
        Retorna 0 se o usuário não tiver um perfil."""
        if self.user and self.user.profiles:
            profile = self.user.profiles[0]
            return profile.calculate_goal(profile.weight)
        return 0

    def add_water(self, water_volume: float):
        """Adiciona um volume de água ao consumo diário."""
        if water_volume <= 0:
            self.events.emit(
                "water_warning",
                "ALERTA! Quantidade de água deve ser maior que zero.")
            return

        self.current_intake += water_volume
        if self.current_intake > self.daily_goal:
            self.current_intake = self.daily_goal
            self.events.emit("water_warning",
                             "ALERTA! Você ultrapassou o consumo diário!")
        
        self.events.emit("water_added", water_volume)

    def reset(self):
        """Reseta o consumo diário de água para zero."""
        self.current_intake = 0

    def get_progress(self):
        """Retorna o progresso do consumo diário em porcentagem. Retorna 0 se
         a meta diária for zero."""
        if self.daily_goal == 0:
            return 0
        return (self.current_intake / self.daily_goal) * 100

    def update(self):
        """Recalcula a meta diária de água."""
        self.daily_goal = self.calculate_daily_goal()
