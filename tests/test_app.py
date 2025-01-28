import pytest
from unittest.mock import MagicMock
from main import MainApp
# from services.water_intake_service import WaterIntakeService
# from services.user_service import UserService
from utils.snackbar_utils import show_snackbar


@pytest.fixture
def app(mocker):
    """Instância do aplicativo com serviços simulados."""
    app = MainApp()
    mocker.patch("utils.snackbar_utils.show_snackbar", side_effect=show_snackbar)
    # mocker.patch("services.water_intake_service.WaterIntakeService", autospec=True)
    # mocker.patch("services.user_service.UserService", autospec=True)
    return app


def test_authenticate_user_success(app, mocker):
    """Testa autenticação bem-sucedida."""
    mock_user = MagicMock()
    mock_user.profile = None
    mock_user.login = "testuser"
    mocker.patch("services.user_service.UserService.load_user", return_value=mock_user)

    app.sm.get_screen("login").ids.login.text = "testuser"
    app.sm.get_screen("login").ids.password.text = "securepass"

    app.authenticate_user()
    assert app.current_user == mock_user
    assert app.sm.current == "create_profile"


def test_authenticate_user_failure(app, mocker):
    """Testa autenticação falha."""
    mocker.patch("services.user_service.UserService.load_user", return_value=None)

    app.sm.get_screen("login").ids.login.text = "wronguser"
    app.sm.get_screen("login").ids.password.text = "wrongpass"

    app.authenticate_user()
    app.show_snackbar.assert_called_once_with("Login ou senha inválidos.")
    assert app.current_user is None
    assert app.sm.current == "login"


def test_save_profile(app, mocker):
    """Testa salvar o perfil do usuário."""
    mock_user = MagicMock()
    mock_user.id = 1
    app.current_user = mock_user

    app.sm.get_screen("create_profile").ids.name.text = "Test User"
    app.sm.get_screen("create_profile").ids.birth_date.text = "1990-01-01"
    app.sm.get_screen("create_profile").ids.weight.text = "70"

    app.save_profile()

    assert app.current_user.profile.name == "Test User"
    assert app.sm.current == "tracker"


def test_add_water_success(app, mocker):
    """Testa adicionar água com sucesso."""
    mock_user = MagicMock()
    mock_user.profile = MagicMock()
    mock_user.profile.daily_goal = 2000
    app.current_user = mock_user
    app.water_tracker = MagicMock()
    app.water_tracker.get_progress.return_value = 50

    mock_water_service = mocker.patch("services.water_intake_service.WaterIntakeService.save_water_intake")

    app.add_water(200)

    mock_water_service.assert_called_once_with(mock_user, 200)
    app.water_tracker.add_water.assert_called_once_with(200)
    assert app.sm.get_screen("tracker").ids.progress_label.text == "Progresso: 200 ml"


def test_add_water_exceeding_goal(app, mocker):
    """Testa adicionar água que excede a meta diária."""
    mock_user = MagicMock()
    mock_user.profile = MagicMock()
    mock_user.profile.daily_goal = 2000
    app.current_user = mock_user
    app.water_tracker = MagicMock()
    app.water_tracker.get_progress.return_value = 100

    app.add_water(2100)

    app.show_snackbar.assert_called_once_with("Você ultrapassou sua meta diária!")
    app.water_tracker.add_water.assert_called_once_with(2100)
    assert app.sm.get_screen("tracker").ids.progress_label.text == "Progresso: 2000 ml"


def test_show_snackbar(mocker):
    """Testa se o Snackbar exibe mensagens corretamente."""
    mock_snackbar = mocker.patch("utils.snackbar_utils.show_snackbar", autospec=True)

    show_snackbar("Mensagem de teste")
    mock_snackbar.assert_called_once_with("Mensagem de teste")
