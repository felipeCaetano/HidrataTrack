import pytest

from models.water_tracker import WaterTracker


def test_user_creation(profile):
    """Testa se o usuário é criado corretamente."""
    assert profile.nome == "Felipe"
    assert profile.genero == "Masculino"
    assert profile.idade == 32
    assert profile.peso == 80
    assert profile.detalhes == "Diabético"

def test_custom_goal_recalculation(profile):
    """Testa se a meta diária recalcula corretamente ao alterar o peso do usuário."""
    tracker = WaterTracker(profile)
    assert tracker.daily_goal == 4000  # 80kg -> 4L

def test_update_weight(profile):
    """Testa a atualização do peso do usuário."""
    profile.update_weight(70)
    assert profile.peso == 70

    # Testa peso inválido
    with pytest.raises(ValueError):
        profile.update_weight(-10)

def test_weight_update_recalculates_goal(profile):
    """Testa se a atualização do peso recalcula a meta no tracker."""
    tracker = WaterTracker(profile)
    assert tracker.daily_goal == 4000  # 80kg -> 4L

    profile.update_weight(60)  # Atualiza o peso
    assert tracker.daily_goal == 3000  # 60kg -> 3L