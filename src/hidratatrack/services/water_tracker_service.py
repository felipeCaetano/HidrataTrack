import logging
from datetime import date


from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from models.models import WaterIntake # NoQA

from services.profile_service import get_profile_byname


class WaterIntakeService:
    def __init__(self, session):
        self.session = session

    def save_water_intake(self, profile, amount):
        """Salva o consumo de água no banco de dados."""
        if not profile:
            raise ValueError("Perfil não encontrado.")
        if amount <= 0:
            raise ValueError("Quantidade de água deve ser maior que zero.")

        intake = WaterIntake(profile_id=profile.id, date=date.today(),
                             amount=amount)
        self.session.add(intake)
        self.session.commit()
        return intake

    def load_daily_intake(self, profile):
        """Carrega o consumo diário total do banco de dados."""
        if not profile:
            raise ValueError("Usuário não pode ser nulo ou inválido.")
        try:
            total = self.session.query(
                func.sum(WaterIntake.amount)
            ).filter(WaterIntake.profile_id == profile.id,
                     func.date(WaterIntake.date) == date.today()).scalar()

            return total or 0  # Retorna 0 se nenhum valor for encontrado
        except SQLAlchemyError as e:
            logging.error(f"Erro ao carregar o consumo diário: {e}")
            raise RuntimeError(f"Falha ao acessar o banco de dados: {str(e)}")

    def reset_daily_intakes(self, profile):
        """Apaga o consumo diário do banco de dados."""
        if not profile:
            raise ValueError("Usuário não pode ser nulo ou inválido.")
        daily_intakes = self.session.scalars(select(WaterIntake).where(
            (WaterIntake.profile_id == profile.id)
            & (func.date(WaterIntake.date) == date.today()))
        ).all()
        for daily_intake in daily_intakes:
            self.session.delete(daily_intake)
        self.session.commit()