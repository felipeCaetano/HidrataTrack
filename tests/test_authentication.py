# import pytest
# from models.models import User
# from models.water_tracker import WaterTracker


# def test_user_creation(valid_user):
#     """Testa se o usuário é criado corretamente."""
#     assert valid_user.login == "valid_user"
#     assert valid_user.password == "secure_password"
#     assert valid_user.profile is None

# # def test_user_set_profile(valid_user):
# #     """Testa se o perfil do usuário é configurado corretamente."""
# #     valid_user.set_profile(name="John Doe", weight=80)
# #     assert valid_user.profile is not None
# #     assert valid_user.profile.nome == "John Doe"
# #     assert valid_user.profile.peso == 80

# def test_valid_user_profile_set_watertracker(valid_user):
#     valid_user.set_profile(name="John Doe", weight=80)
#     tracker = WaterTracker(valid_user.profile)
#     assert tracker.daily_goal == 4000  # 80kg -> 4L

# # def test_update_password(valid_user):
# #     """Testa se a senha do usuário é atualizada corretamente."""
# #     valid_user.update_password("new_secure_password")
# #     assert valid_user.password == "new_secure_password"

# def test_authenticate_user_success(valid_user):
#     """Testa a autenticação com credenciais válidas."""
#     user = User(**valid_user)
#     assert user.login == valid_user.login
#     assert user.password == valid_user.password

# def test_authenticate_user_failure(valid_user):
#     """Testa a autenticação com credenciais inválidas."""
#     login, email, password = "invalid_user", "valid@email.com", "wrong_password"
#     user = User(login="valid_user", email=email, password="secure_password")
#     assert not (user.login == login and user.password == password)
