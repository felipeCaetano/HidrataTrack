import logging
from datetime import date

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models.models import WaterIntake

from src.hidratatrack.services.profile_service import get_profile_byname


class WaterIntakeService:
    def __init__(self, session):
        self.session = session

    def save_water_intake(self, profile_name, amount):
        """Salva o consumo de água no banco de dados."""
        if not profile_name:
            raise ValueError("Perfil não encontrado.")
        if amount <= 0:
            raise ValueError("Quantidade de água deve ser maior que zero.")

        profile = get_profile_byname(profile_name)
        intake = WaterIntake(profile_id=profile.id, date=date.today(),
                             amount=amount, profile=profile)
        logging.debug(f'{profile_name}, {profile.name}')
        self.session.add(intake)
        self.session.commit()
        return intake

    def load_daily_intake(self, profile):
        """Carrega o consumo diário total do banco de dados."""
        if not profile:
            raise ValueError("Usuário não pode ser nulo ou inválido.")

        try:
            # Realiza a consulta para obter o consumo total
            total = self.session.query(
                func.sum(WaterIntake.amount)
            ).filter(
                # fazer o ajuste de capturar o profile
                WaterIntake.profile_id == profile.id,
                func.date(WaterIntake.date) == date.today()
            ).scalar()

            return total or 0  # Retorna 0 se nenhum valor for encontrado

        except SQLAlchemyError as e:
            # Loga o erro e relança uma exceção
            print(f"Erro ao carregar o consumo diário: {e}")
            raise RuntimeError("Falha ao acessar o banco de dados.")
