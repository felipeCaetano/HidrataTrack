from src.hidratatrack.models.user import AppUser
from src.hidratatrack.models.water_tracker import WaterTracker
from src.hidratatrack.models.perfil import Profile


from src.hidratatrack.main import MainApp

def test_authenticate_user(test_session):
    """Testa o fluxo de autenticação."""
    app = MainApp()
    user = AppUser(login="testuser", password="testpass")
    test_session.add(user)
    test_session.commit()

    app.sm.get_screen("login").ids.login.text = "testuser"
    app.sm.get_screen("login").ids.password.text = "testpass"
    app.authenticate_user()

    assert app.user is not None
    assert app.user.login == "testuser"

def test_create_profile(test_session):
    """Testa a criação de um perfil via aplicativo."""
    app = MainApp()
    user = AppUser(login="testuser", password="testpass")
    test_session.add(user)
    test_session.commit()

    app.user = user
    app.sm.get_screen("create_profile").ids.name.text = "Test User"
    app.sm.get_screen("create_profile").ids.birth_date.text = "01/01/1990"
    app.sm.get_screen("create_profile").ids.weight.text = "70"

    app.create_profile()

    stored_profile = test_session.query(Profile).filter_by(user_id=user.id).first()
    assert stored_profile.name == "Test User"
    assert stored_profile.weight == 70.0
