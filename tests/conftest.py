from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.hidratatrack.models.models import Base, session, Profile, WaterIntake
from src.hidratatrack.models.perfil import Profile
from src.hidratatrack.models.user import AppUser
from src.hidratatrack.models.water_tracker import WaterTracker


@pytest.fixture
def valid_user():
    """Fixture para criar um usuário válido."""
    user = AppUser(login="valid_user", password="secure_password")
    return user


@pytest.fixture
def profile():
    """Cria um usuário fictício para os testes."""
    return Profile(
        nome="Felipe",
        genero="Masculino",
        data_nascimento=date(1993, 1, 1),
        peso=80,
        detalhes="Diabético"
    )


@pytest.fixture
def tracker(profile):
    return WaterTracker(profile)


@pytest.fixture
def setup_database():
    """Configuração inicial do banco para testes."""
    session.query(WaterIntake).delete()
    session.query(Profile).delete()
    session.query(AppUser).delete()
    session.commit()

    user = AppUser(login="testuser", password="testpass")
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
def test_session():
    """Configura um banco de dados SQLite temporário para os testes."""
    engine = create_engine("sqlite:///:memory:")  # Banco de dados em memória
    Base.metadata.create_all(engine)  # Cria todas as tabelas

    Session = sessionmaker(bind=engine) # NoQA
    session = Session()

    yield session  # Fornece a sessão para os testes

    session.close()  # Fecha a sessão após o teste
    engine.dispose()  # Limpa o banco de dados
