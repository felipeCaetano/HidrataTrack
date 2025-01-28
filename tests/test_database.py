# import pytest
# from datetime import date
# from models.models import session, User, Profile, WaterIntake


# def test_user_creation(valid_user):
#     """Testa a criação de um usuário."""
#     user = valid_user
#     assert user.id is not None
#     assert user.login == "testuser"

# def test_profile_creation(profile):
#     """Testa a criação de um perfil."""
#     assert profile.id is not None
#     assert profile.name == "Test User"
#     assert profile.weight == 70.0

# def test_water_intake(valid_user):
#     """Testa o registro de consumo de água."""
#     intake = WaterIntake(user_id=valid_user.id, date=date.today(), amount=250)
#     session.add(intake)
#     session.commit()

#     stored_intake = session.query(WaterIntake).filter_by(user_id=valid_user.id).first()
#     assert stored_intake.amount == 250
#     assert stored_intake.date == date.today()
