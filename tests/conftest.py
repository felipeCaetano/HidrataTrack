from datetime import date
import pytest

from src.hidratatrack.water_tracker import WaterTracker
from src.hidratatrack.profile import Profile
from src.hidratatrack.user import User


@pytest.fixture
def valid_user():
    """Fixture para criar um usuário válido."""
    user = User(login="valid_user", password="secure_password")
    return user


@pytest.fixture
def profile():
    """Cria um usuário fictício para os testes."""
    return Profile(nome="Felipe", genero="Masculino",
                   data_nascimento=date(1993, 1, 1), peso=80,
                   detalhes="Diabético")


@pytest.fixture
def tracker(user):
    return WaterTracker(user)
