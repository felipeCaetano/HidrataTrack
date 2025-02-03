from datetime import date, datetime
from unittest.mock import MagicMock

import pytest
from kivy.base import EventLoop
from kivymd.app import MDApp
from main import MainApp
from models.models import (Profile, table_registry, User)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture
def session():
    """Cria um banco de dados em memória para testes."""
    test_engine = create_engine("sqlite:///:memory:")  # Banco em memória
    table_registry.metadata.create_all(test_engine)  # Cria as tabelas
    with Session(test_engine) as session:
        yield session
    test_engine.dispose()  # Fecha a conexão ao final dos testes
    table_registry.metadata.drop_all(test_engine)


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
def test_session(session):
    """Cria uma sessão conectada ao banco de dados em memória."""
    TestSession = sessionmaker(bind=session)
    session = TestSession()

    # Fornece a sessão para o teste
    yield session
    # Limpa a sessão após o teste
    session.close()


@pytest.fixture
def app():
    """Inicializa a MainApp sem iniciar o loop de eventos."""
    EventLoop.ensure_window()
    app = MainApp()
    # Garante que o loop de eventos do Kivy está configurado para o teste
    app.root = app.build()
    return app