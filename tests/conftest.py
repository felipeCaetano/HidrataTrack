from datetime import date, datetime
from unittest.mock import MagicMock
from kivymd.app import MDApp
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import (Profile, User, table_registry)


@pytest.fixture
def test_engine():
    """Cria um banco de dados em memória para testes."""
    test_engine = create_engine("sqlite:///:memory:")  # Banco em memória
    table_registry.metadata.create_all(test_engine)  # Cria as tabelas
    yield test_engine
    test_engine.dispose()  # Fecha a conexão ao final dos testes


@pytest.fixture
def valid_user(test_session):
    """Fixture para criar um usuário válido."""
    user = User(
        login="valid_user",
        email="valid@mail.com",
        password="secure_password"
    )
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def profile(valid_user):
    """Cria um usuário fictício para os testes."""
    profile = Profile(
        name="Felipe",
        gender="Masculino",
        birth_date=date(1993, 1, 1),
        weight=80,
        details="Diabético\nPai",
        user_id=valid_user.id,
        user=valid_user
    )
    return profile


@pytest.fixture
def user_with_profile():
    user = User(login="testuser", email="test@example.com", password="securepass")
    profile = Profile(
        user_id=user.id,
        name="Felipe",
        birth_date=datetime(1990, 1, 1),
        gender="Masculino",
        weight=80,
        details="Teste",
        user=user
    )
    user.profiles = [profile]
    return user


# Mock do MDApp
@pytest.fixture
def mock_app():
    mock_app = MagicMock()
    mock_app.user = None
    mock_app.daily_goal = 0
    mock_app.progress = 0
    return mock_app


@pytest.fixture(autouse=True)
def mock_kivymd(mocker):
    """Configura o mock do KivyMD para todos os testes."""
    mock_app = MagicMock()
    mocker.patch.object(MDApp, 'get_running_app', return_value=mock_app)
    return mock_app


@pytest.fixture()
def test_session(test_engine):
    """Cria uma sessão conectada ao banco de dados em memória."""
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()

    # Fornece a sessão para o teste
    yield session
    # session.rollback() 
    # Fecha a sessão e limpa os mapeamentos ao final
    # session.close()
    # clear_mappers()

# @pytest.fixture
# def mock_screen():
#     """Creates a mock screen with required ids."""
#     screen = MagicMock()
#     screen.ids = {
#         'login': MagicMock(text=''),
#         'password': MagicMock(text=''),
#         'name': MagicMock(text=''),
#         'birth_date': MagicMock(text=''),
#         'weight': MagicMock(text=''),
#         'progress_label': MagicMock(text='')
#     }
#     return screen

# @pytest.fixture
# def app(mocker, mock_screen):
#     """Instância do aplicativo com serviços simulados."""
#     app = MainApp()

#     # Mock the screen manager and screens
#     app.root = MagicMock()
#     # app.sm = app.root  # Assuming sm is an alias for root in your app

#     # Set up the mock screens
#     screens = {
#         'login': mock_screen,
#         'create_profile': mock_screen,
#         'tracker': mock_screen
#     }
#     app.root.get_screen.side_effect = lambda name: screens[name]

#     mocker.patch("utils.snackbar_utils.show_snackbar", side_effect=show_snackbar)
#     return app
