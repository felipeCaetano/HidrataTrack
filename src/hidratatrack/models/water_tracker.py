from kivymd.app import MDApp

from models.models import User


class WaterTracker:
    def __init__(self):
        self.app = MDApp.get_running_app()
        if self.app.user and self.app.user.profiles:
            self.app.daily_goal = self.calculate_daily_goal()
            self.current_intake = self.app.load_daily_intake(self.app.user)
            self.app.progress = self.get_progress()
        else:
             print("Sem perfil?")
             self.app.daily_goal = 0

    def calculate_daily_goal(self):
        if self.app.user and self.app.user.profiles:
            return self.app.user.profiles.calculate_goal(
                self.app.user.profiles.weight)
        else:
             print("sem perfl?")
             return 0

    def add_water(self, water_volume: float):
        if water_volume <= 0:
            print("ALERTA! Quantidade de água deve ser maior que zero.")
            return

        self.current_intake += water_volume
        if self.current_intake > self.app.daily_goal:
            self.current_intake = self.app.daily_goal
            print("ALERTA! Você ultrapassou o consumo diário!")
        
    def reset(self):
        self.current_intake = 0
    
    def get_progress(self):
        print(f'{self.current_intake=}')
        return (self.current_intake/self.app.daily_goal) * 100
    
    def update(self):
        """Método chamado quando o Observable notifica seus observadores"""
        self.app.daily_goal = self.calculate_daily_goal()