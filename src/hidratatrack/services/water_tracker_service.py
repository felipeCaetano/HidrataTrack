from datetime import date

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models.models import WaterIntake


class WaterIntakeService:
    def __init__(self, session):
        self.session = session

    def save_water_intake(self, user, amount):
        """Salva o consumo de água no banco de dados."""
        if not user:
            raise ValueError("Usuário não encontrado.")
        if amount <= 0:
            raise ValueError("Quantidade de água deve ser maior que zero.")
        
        intake = WaterIntake(
            profile_id=user.profiles[0].id, date=date.today(), amount=amount,
            profile=user.profiles[0]
            )
        self.session.add(intake)
        self.session.commit()
        return intake

    def load_daily_intake(self, user):
        """Carrega o consumo diário total do banco de dados."""
        if not user:
            raise ValueError("Usuário não pode ser nulo ou inválido.")

        try:
            # Realiza a consulta para obter o consumo total
            total = self.session.query(
                func.sum(WaterIntake.amount)
            ).filter(
                WaterIntake.user_id == user.id,
                func.date(WaterIntake.date) == date.today()
            ).scalar()

            return total or 0  # Retorna 0 se nenhum valor for encontrado

        except SQLAlchemyError as e:
            # Loga o erro e relança uma exceção
            print(f"Erro ao carregar o consumo diário: {e}")
            raise RuntimeError("Falha ao acessar o banco de dados.")
