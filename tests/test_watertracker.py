from unittest.mock import Mock

from services.water_tracker import WaterTracker # NoQA


def test_calculate_daily_goal(user_with_profile):
    """Testa o cálculo da meta diária de água."""
    tracker = WaterTracker(user=user_with_profile)
    assert tracker.calculate_daily_goal(None) == 4000  # 80kg -> 4L


def test_calculate_daily_goal_no_profile(valid_user):
    """Testa o cálculo da meta diária quando o usuário não tem perfil."""
    tracker = WaterTracker(user=valid_user)
    assert tracker.calculate_daily_goal(None) == 0


def test_add_water(user_with_profile):
    
    tracker = WaterTracker(user=user_with_profile)
    tracker.add_water(500)
    assert tracker.current_intake == 500
    assert tracker.get_progress() == 12.5

def test_add_water_exceeds_daily_goal(user_with_profile, mock_kivymd):
    """Testa a adição de água que excede a meta diária."""
    tracker = WaterTracker(user=user_with_profile)
    warning_handler = Mock()
    tracker.events.on("water_warning", warning_handler)
    
    mock_kivymd.user = user_with_profile
    mock_kivymd.daily_goal = 4000  # Meta diária de 4L
    
    tracker.add_water(5000)

    warning_handler.assert_called_once_with(
        "ALERTA! Você ultrapassou o consumo diário!")
    assert tracker.current_intake == tracker.daily_goal

def test_add_water_negative_value(user_with_profile, mock_kivymd):
    """Testa a adição de um valor negativo de água."""
    tracker = WaterTracker(user=user_with_profile)
    warning_handler = Mock()
    tracker = WaterTracker(user=user_with_profile)
    tracker.events.on("water_warning", warning_handler)

    tracker.add_water(-500)
    # Assert
    warning_handler.assert_called_once_with(
        "ALERTA! Quantidade de água deve ser maior que zero.")
    assert tracker.current_intake == 0  # Valor negativo não deve ser adicionado

def test_reset(user_with_profile):
    """Testa o reset do consumo diário de água."""
    tracker = WaterTracker(user=user_with_profile)
    tracker.add_water(500)
    tracker.reset()
    assert tracker.current_intake == 0

def test_get_progress_no_goal(valid_user):
    """Testa o cálculo do progresso quando a meta diária é zero."""
    tracker = WaterTracker(user=valid_user)
    assert tracker.get_progress() == 0

def test_update_daily_goal(user_with_profile):
    """Testa a atualização da meta diária de água."""
    tracker = WaterTracker(user=user_with_profile)
    tracker.update()
    assert tracker.daily_goal == 4000  # 80kg -> 4L