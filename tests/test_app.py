from src.hidratatrack.water_tracker import WaterTracker


def test_initial_state(tracker):
    """Testa se o estado inicial é zero."""
    assert tracker.current_intake == 0
    assert tracker.daily_goal == 4000

def test_add_water(tracker):
    """Testa se adicionar água aumenta corretamente o consumo."""
    tracker.add_water(225)
    assert tracker.current_intake == 225

def test_add_water_exceeding_goal(tracker):
    """Testa se o consumo não ultrapassa a meta diária."""
    tracker.add_water(4000)
    assert tracker.current_intake == 4000

def test_reset(tracker):
    """Testa se o reset zera o consumo diário."""
    tracker.add_water(225)
    tracker.reset()
    assert tracker.current_intake == 0

def test_progress(tracker):
    """Testa o cálculo de progresso percentual."""
    tracker.add_water(2000)
    assert tracker.get_progress() == 50

def test_add_negative_water(tracker):
    """Testa se valores negativos não alteram o consumo."""
    tracker.add_water(-225)
    assert tracker.current_intake == 0

def test_add_zero_water(tracker):
    """Testa se adicionar zero não altera o consumo."""
    tracker.add_water(0)
    assert tracker.current_intake == 0

def test_progress_does_not_exceed_100(tracker):
    """Testa se o progresso nunca ultrapassa 100%."""
    tracker.add_water(4000)
    assert tracker.get_progress() == 100

def test_custom_goal_recalculation(profile):
    """Testa se a meta diária recalcula corretamente ao alterar o peso do usuário."""
    tracker = WaterTracker(profile)
    assert tracker.daily_goal == 4000  # 80kg -> 4L

    profile.peso = 60  # Altera o peso do usuário
    tracker.daily_goal = tracker.calculate_daily_goal()  # Recalcula a meta
    assert tracker.daily_goal == 3000  # 60kg -> 3L

from unittest.mock import Mock
from src.hidratatrack.main import HidrataTrackApp

def test_login_with_existing_profile():
    """Testa se o login com um perfil existente redireciona para a tela de rastreamento."""
    # Inicializar o aplicativo
    app = HidrataTrackApp()
    app.build()

    # Mockar o usuário com um perfil existente
    app.user = Mock()
    # app.user.profile = {
    #     "nome": "Test User",
    #     "peso": 70,
    #     "data_nascimento": "1990-01-01",
    #     "genero": "Masculino",
    #     "detalhes": []
    # }
    app.user.set_profile("Test User", 70)

    # Mockar as credenciais de login
    app.sm.get_screen("login").ids.login.text = "test"
    app.sm.get_screen("login").ids.password.text = "1234"

    # Autenticar o usuário
    app.authenticate_user()

    # Verificar se a tela foi trocada para o rastreador
    assert app.sm.current == "tracker", "O login com perfil existente não redirecionou para a tela de rastreamento"
