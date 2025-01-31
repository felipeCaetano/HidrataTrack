from datetime import datetime
from pprint import pprint

import pytest

# from models.water_tracker import WaterTracker

from models.models import Profile, User, WaterIntake
from datetime import datetime, date
from models.models import Profile


def test_user_creation(valid_user):
    """Testa se o usuário é criado corretamente."""
    assert valid_user.login == "valid_user"
    assert valid_user.password == "secure_password"
    assert valid_user.profiles == []


def test_profile_creation(valid_user):
    stored_user = valid_user
    profile = Profile(
        user_id=valid_user.id, name='Felipe',
        birth_date=datetime(1990, 1, 1),
        gender='Masculino', weight=80,
        details="", user=stored_user)
    assert profile is not None
    assert profile.user.email == "valid@mail.com"


def test_profile_age_calculation(profile):
    """Testa o cálculo da idade do perfil."""
    assert profile.get_age() == 32



def test_get_age_before_birthday(profile):
    """Testa se get_age() subtrai corretamente 1 ano quando o aniversário ainda
    não passou."""
    today = date.today()
    # Criamos um perfil com data de nascimento futura no ano atual
    profile.birth_date = date(1990, 3, 30)

    assert profile.get_age() == today.year - profile.birth_date.year - 1  # Deve subtrair 1


def test_profile_calculate_goal(profile):
    """Testa o cálculo da meta diária de água."""
    assert profile.calculate_goal(80) == 4000  # 80kg -> 4L


def test_profile_update_weight(profile):
    """Testa a atualização do peso do perfil."""

    profile.update_weight(70)
    assert profile.weight == 70

    # Testa se um peso inválido lança uma exceção
    with pytest.raises(ValueError):
        profile.update_weight(-10)


def test_water_intake_negative_amount(profile):
    """Testa se um valor negativo para WaterIntake levanta um erro."""
    with pytest.raises(ValueError):
        WaterIntake(
            profile_id=1,
            date=datetime(2024, 1, 1),
            amount=-500, profile=profile)
