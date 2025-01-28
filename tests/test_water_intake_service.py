# from datetime import date
# from sqlalchemy.exc import SQLAlchemyError
# from models.models import User, WaterIntake
# from services.water_intake_service import WaterIntakeService

# # def test_load_daily_intake_valid_user(test_session):
# #     """Testa carregar o consumo diário para um usuário válido."""
# #     user = User(login="testuser", password="securepass")
# #     test_session.add(user)
# #     test_session.commit()

# #     # Adiciona registros de consumo
# #     intake1 = WaterIntake(user_id=user.id, date=date.today(), amount=200)
# #     intake2 = WaterIntake(user_id=user.id, date=date.today(), amount=300)
# #     test_session.add_all([intake1, intake2])
# #     test_session.commit()

# #     service = WaterIntakeService(test_session)
# #     total = service.load_daily_intake(user)
# #     assert total == 500

# def test_load_daily_intake_no_data(test_session):
#     """Testa carregar o consumo diário quando não há dados."""
#     user = User(login="testuser", password="securepass")
#     test_session.add(user)
#     test_session.commit()

#     service = WaterIntakeService(test_session)
#     total = service.load_daily_intake(user)
#     assert total == 0

# def test_load_daily_intake_invalid_user(test_session):
#     """Testa carregar o consumo diário para um usuário inválido."""
#     service = WaterIntakeService(test_session)
#     with pytest.raises(ValueError, match="Usuário não pode ser nulo ou inválido."):
#         service.load_daily_intake(None)

# def test_load_daily_intake_database_error(test_session, mocker):
#     """Testa falha de consulta ao banco de dados."""
#     user = User(login="testuser", password="securepass")
#     test_session.add(user)
#     test_session.commit()

#     mocker.patch.object(test_session, "query", side_effect=SQLAlchemyError("DB error"))
#     service = WaterIntakeService(test_session)

#     with pytest.raises(RuntimeError, match="Falha ao acessar o banco de dados."):
#         service.load_daily_intake(user)
