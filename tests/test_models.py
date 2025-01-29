from datetime import datetime
from pprint import pprint

import pytest

# from models.water_tracker import WaterTracker


# def test_user_creation(profile):
#     """Testa se o usuário é criado corretamente."""
#     assert profile.name == "Felipe"
#     assert profile.gender == "Masculino"
#     assert profile.birth_date == datetime.date(1993, 1, 1)
#     assert profile.weight == 80
#     assert profile.details == "Diabético"


# def test_custom_goal_recalculation():
#     """Testa se a meta diária recalcula corretamente
#     ao alterar o peso do usuário."""
#     tracker = WaterTracker()
#     assert tracker.daily_goal == 4000  # 80kg -> 4L


# def test_update_weight(profile):
#     """Testa a atualização do peso do usuário."""
#     profile.update_weight(70)
#     assert profile.weight == 70

#     # Testa peso inválido
#     with pytest.raises(ValueError):
#         profile.update_weight(-10)


# def test_weight_update_recalculates_goal(profile):
#     """Testa se a atualização do peso recalcula a meta no tracker."""
#     tracker = WaterTracker()
#     assert tracker.daily_goal == 4000  # 80kg -> 4L

#     profile.update_weight(60)  # Atualiza o peso
#     assert tracker.daily_goal == 3000  # 60kg -> 3L
from models.models import Profile, User, WaterIntake


def test_user_creation(test_session):
    """Testa a criação de um usuário."""
    user = User(login="testuser", email="test@example.com",
                password="securepass")
    test_session.add(user)
    test_session.commit()

    stored_user = test_session.query(User).filter_by(login="testuser").first()
    assert stored_user is not None
    assert stored_user.email == "test@example.com"


def test_profile_creation(valid_user):
    stored_user = valid_user
    profile = Profile(
        user_id=valid_user.id, name='Felipe',
        birth_date=datetime(1990, 1, 1),
        gender='Masculino', weight=80,
        details="", user=stored_user)
    assert profile is not None
    assert profile.user.email == "valid@mail.com"


def test_profile_save(valid_user, test_session):
    stored_user = valid_user
    profile = Profile(
        user_id=valid_user.id, name='Felipe',
        birth_date=datetime(1990, 1, 1),
        gender='Masculino', weight=80,
        details="", user=stored_user)
    test_session.add(profile)
    test_session.commit()
    user = test_session.query(User).filter_by(id=valid_user.id).first()
    assert len(user.profiles) == 1
    assert user.profiles[0].name == "Felipe"


def test_user_with_profiles(test_session, valid_user, profile):
    """Testa associar múltiplos perfis a um usuário."""
    # Cria perfis associados ao usuário
    profile1 = profile
    profile2 = Profile(
        user_id=valid_user.id, name="Miguel",
        birth_date=datetime(2015, 6, 10), gender="Masculino",
        weight=30, details="Filho", user=valid_user
    )
    test_session.add_all([profile1, profile2])
    test_session.commit()

    # Recupera o usuário e verifica os perfis associados
    user = test_session.query(User).filter_by(id=valid_user.id).first()
    assert len(user.profiles) == 2
    assert user.profiles[0].name == "Felipe"
    assert user.profiles[1].name == "Miguel"


def test_profile_age_calculation(profile):
    """Testa o cálculo da idade do perfil."""
    assert profile.get_age() == 32


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


def test_water_intake_creation(test_session, valid_user):
    """Testa a criação de um registro de ingestão de água."""
    # Cria um registro de ingestão de água
    water_intake = WaterIntake(
        user_id=valid_user.id,
        date=datetime(2023, 10, 1),
        amount=500.0
    )
    test_session.add(water_intake)
    test_session.commit()

    # Verifica se o registro foi salvo corretamente
    stored_intake = test_session.query(WaterIntake).filter_by(
        user_id=valid_user.id).first()
    assert stored_intake is not None
    assert stored_intake.amount == 500.0
    assert stored_intake.date == datetime(2023, 10, 1)


def test_water_intake_user_association(test_session, valid_user):
    """Testa a associação de um registro de ingestão de água com um usuário."""
    # Cria um registro de ingestão de água
    water_intake = WaterIntake(
        user_id=valid_user.id,
        date=datetime(2023, 10, 1),
        amount=500.0
    )
    test_session.add(water_intake)
    test_session.commit()

    # Verifica se o registro está associado ao usuário correto
    user = test_session.query(User).filter_by(id=valid_user.id).first()
    assert len(user.water_intakes) == 1
    assert user.water_intakes[0].amount == 500.0


def test_multiple_water_intakes(test_session, valid_user):
    """Testa a criação de múltiplos registros de ingestão de água
    para um usuário."""
    # Cria dois registros de ingestão de água
    water_intake1 = WaterIntake(
        user_id=valid_user.id,
        date=datetime(2023, 10, 1),
        amount=500.0
    )
    water_intake2 = WaterIntake(
        user_id=valid_user.id,
        date=datetime(2023, 10, 2),
        amount=1000.0
    )
    test_session.add(water_intake1)
    test_session.add(water_intake2)
    test_session.commit()

    # Verifica se os registros foram salvos e associados ao usuário
    water_intakes = test_session.query(WaterIntake).all()
    assert len(water_intakes) == 2
    assert water_intakes[0].amount == 500.0
    assert water_intakes[1].amount == 1000.0


def test_water_intake_negative_amount(test_session, valid_user):
    """Testa se um valor negativo para amount lança uma exceção."""
    with pytest.raises(ValueError):
        water_intake = WaterIntake(
            user_id=valid_user.id,
            date=datetime(2023, 10, 1),
            amount=-500.0  # Valor negativo deve lançar uma exceção
        )
        test_session.add(water_intake)
        test_session.commit()
