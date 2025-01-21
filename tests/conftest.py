from datetime import date
import pytest

from models.water_tracker import WaterTracker
from models.perfil import Profile
from models.user import User


@pytest.fixture
def valid_user():
    """Fixture para criar um usuário válido."""
    user = User(login="valid_user", password="secure_password")
    return user

@pytest.fixture
def profile():
    """Cria um usuário fictício para os testes."""
    return Profile(nome="Felipe", genero="Masculino", data_nascimento=date(1993, 1, 1), peso=80, detalhes="Diabético")

@pytest.fixture
def tracker(profile):
    return WaterTracker(profile)

