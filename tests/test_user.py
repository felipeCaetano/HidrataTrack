import pytest

from src.hidratatrack.water_tracker import WaterTracker


def test_user_creation(user):
    """Testa se o usuário é criado corretamente."""
    assert user.nome == "Felipe"
    assert user.genero == "Masculino"
    assert user.idade == 32
    assert user.peso == 80
    assert user.detalhes == "Diabético"

def test_custom_goal_recalculation(user):
    """Testa se a meta diária recalcula corretamente ao alterar o peso do usuário."""
    tracker = WaterTracker(user)
    assert tracker.daily_goal == 4000  # 80kg -> 4L

def test_update_weight(user):
    """Testa a atualização do peso do usuário."""
    user.update_weight(70)
    assert user.peso == 70

    # Testa peso inválido
    with pytest.raises(ValueError):
        user.update_weight(-10)

def test_weight_update_recalculates_goal(user):
    """Testa se a atualização do peso recalcula a meta no tracker."""
    tracker = WaterTracker(user)
    assert tracker.daily_goal == 4000  # 80kg -> 4L

    user.update_weight(60)  # Atualiza o peso
    assert tracker.daily_goal == 3000  # 60kg -> 3L