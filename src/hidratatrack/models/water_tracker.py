from models.user import User


class WaterTracker:
    def __init__(self, user: User):
        self.current_intake = 0
        self.user = user
        self.user.profile.add_observer(self)
        self.daily_goal = self.calculate_daily_goal()

    def calculate_daily_goal(self):
        return self.user.profile.daily_goal

    def add_water(self, water_volume: float):
        if water_volume > 0:
             self.current_intake += water_volume
        else:
            print("ALERTA! Não Permitido: Quantidade de água deve ser maior que Zero.")
        if self.current_intake > self.daily_goal:
            self.current_intake = self.daily_goal
            print("ALERTA! Você ultrapassou o consumo diário!")
        
    def reset(self):
        self.current_intake = 0
    
    def get_progress(self):
        return (self.current_intake/self.daily_goal) * 100
    
    def update(self):
        """Recalcula a meta diária ao ser notificado."""
        self.daily_goal = self.calculate_daily_goal()