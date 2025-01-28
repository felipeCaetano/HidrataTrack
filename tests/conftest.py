from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from models.models import Profile, User, WaterIntake, table_registry, engine, session
from models.water_tracker import WaterTracker


@pytest.fixture(scope="function")
def test_engine():
    """Cria um banco de dados em memória para testes."""
    test_engine = create_engine("sqlite:///:memory:")  # Banco em memória
    table_registry.metadata.create_all(test_engine)  # Cria as tabelas
    yield test_engine
    test_engine.dispose()  # Fecha a conexão ao final dos testes


@pytest.fixture
def valid_user():
    """Fixture para criar um usuário válido."""
    user = User(
        login="valid_user",
        email="valid@mail.com",
        password="secure_password"
        )
    return user


@pytest.fixture
def profile():
    """Cria um usuário fictício para os testes."""
    return Profile(
        name="Felipe",
        gender="Masculino",
        birth_date=date(1993, 1, 1),
        weight=80,
        details="Diabético"
    )


@pytest.fixture
def tracker(profile):
    return WaterTracker(profile)


@pytest.fixture
def setup_database():
    """Configuração inicial do banco para testes."""
    session.query(WaterIntake).delete()
    session.query(Profile).delete()
    session.query(User).delete()
    session.commit()

    user = User(valid_user)
    session.add(user)
    session.commit()

    profile = Profile(
        user_id=user.id,
        name="Test User",
        birth_date=date(1990, 1, 1),
        weight=70.0,
        details="Teste"
    )
    session.add(profile)
    session.commit()

    return user, profile


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Cria uma sessão conectada ao banco de dados em memória."""
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()

    # Fornece a sessão para o teste
    yield session

    # Fecha a sessão e limpa os mapeamentos ao final
    session.close()
    clear_mappers()
