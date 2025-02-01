from datetime import datetime

from services.user_service import create_user, get_user
from services.profile_service import create_profile, save_profile

from models.models import User
from services.user_service import save_user


def test_create_user(test_session):
    """Testa se um usuário é criado corretamente via user_service."""
    user = create_user("newuser", "newuser@mail.com", "securepass")

    assert user is not None
    assert user.email == "newuser@mail.com"


def test_save_user(valid_user):
    """Testa se conseguimos salvar um usuário corretamente via user_service."""
    user = User("newuser", "newuser@mail.com", "securepass")
    user = save_user(user)

    assert user is not None
    assert user.emapiil == "newuser@mail.com"

    user = save_user(valid_user)
    assert user.login == valid_user.login


def test_get_user_by_email(test_session, valid_user):
    """Testa se conseguimos buscar um usuário pelo e-mail."""
    user = get_user(valid_user.email, test_session)
    assert user is not None
    assert user.email == valid_user.email


def test_get_user_by_login(test_session, valid_user):
    """Testa se conseguimos buscar um usuário pelo login."""
    user = get_user(valid_user.login, test_session)
    assert user is not None
    assert user.login == valid_user.login


def test_save_profile(test_session, valid_user):
    """Testa se conseguimos salvar um perfil corretamente via profile_service."""
    date_obj = datetime(1990, 1, 1)
    new_profile = create_profile(valid_user, profile_name="Felipe",
                             date_obj=date_obj, gender="Masculino",
                             weight=80, details="Detalhes")
    profile_db = save_profile(
        user=valid_user,
        profile=new_profile
    )

    assert profile_db is not None
    assert profile_db.name == "Felipe"
    assert profile_db.weight == 80
    assert profile_db.user_id == valid_user.id
