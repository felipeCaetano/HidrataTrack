import pytest
from datetime import date
from models.models import session, User, Profile, WaterIntake


def test_user_creation(setup_database):
    """Testa a criação de um usuário."""
    user, _ = setup_database
    assert user.id is not None
    assert user.login == "testuser"

def test_profile_creation(setup_database):
    """Testa a criação de um perfil."""
    _, profile = setup_database
    assert profile.id is not None
    assert profile.name == "Test User"
    assert profile.weight == 70.0

def test_water_intake(setup_database):
    """Testa o registro de consumo de água."""
    user, _ = setup_database
    intake = WaterIntake(user_id=user.id, date=date.today(), amount=250)
    session.add(intake)
    session.commit()

    stored_intake = session.query(WaterIntake).filter_by(user_id=user.id).first()
    assert stored_intake.amount == 250
    assert stored_intake.date == date.today()
