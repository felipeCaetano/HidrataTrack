from datetime import datetime
import pytest
from models.models import Profile, User, WaterIntake
from sqlalchemy.exc import IntegrityError


def test_user_save_in_db(test_session):
    """Testa a criação de um usuário."""
    user = User(login="testuser", email="test@example.com",
                password="securepass")
    test_session.add(user)
    test_session.commit()

    stored_user = test_session.query(User).filter_by(login="testuser").first()
    assert stored_user is not None
    assert stored_user.email == "test@example.com"


def test_user_deletation(test_session, valid_user):
    # Deletar o usuário
    test_session.delete(valid_user)
    test_session.commit()

    # Verificar se o usuário foi realmente deletado
    deleted_user = test_session.query(User).filter_by(id=valid_user.id).first()
    assert deleted_user is None  # Usuário deve ser removido


def test_unique_email_constraint(test_session):
    """Testa se o banco impede e-mails duplicados."""
    
    # Criar primeiro usuário
    user1 = User(login="user1", email="duplicate@mail.com", password="1234")
    test_session.add(user1)
    test_session.commit()

    # Criar segundo usuário com o mesmo e-mail
    user2 = User(login="user2", email="duplicate@mail.com", password="5678")
    test_session.add(user2)

    # Deve falhar ao tentar salvar
    with pytest.raises(IntegrityError):
        test_session.commit()

    test_session.rollback()


def test_unique_login_constraint(test_session):
    """Testa se o banco impede logins duplicados."""

    # Criar primeiro usuário
    user1 = User(login="repeated_login", email="user1@mail.com", password="1234")
    test_session.add(user1)
    test_session.commit()

    # Criar segundo usuário com o mesmo login
    user2 = User(login="repeated_login", email="user2@mail.com", password="5678")
    test_session.add(user2)

    # Deve falhar ao tentar salvar
    with pytest.raises(IntegrityError):
        test_session.commit()

    test_session.rollback()


def test_profile_save_in_db(valid_user, test_session):
    stored_user = valid_user
    profile = Profile(
        user_id=valid_user.id,
        name='Felipe',
        birth_date=datetime(1990, 1, 1),
        gender='Masculino',
        weight=80,
        details="",
        user=stored_user)
    test_session.add(profile)
    test_session.commit()
    user = test_session.query(User).filter_by(id=valid_user.id).first()
    assert len(user.profiles) == 1
    assert user.profiles[0].name == "Felipe"


def test_profile_missing_name(test_session, valid_user):
    # Criar perfil sem nome
    with pytest.raises(TypeError):
        profile = Profile(
            user_id=valid_user.id, birth_date=datetime(1995, 5, 15),
            gender="Feminino", weight=65, details="", user=valid_user
        )
        test_session.add(profile)
        test_session.commit()
    
    test_session.rollback()


def test_profile_missing_birth_Date(test_session, valid_user):
    # Criar perfil sem data de nascimento
    with pytest.raises(TypeError):
        profile = Profile(
            user_id=valid_user.id, name="Teste",
            gender="Feminino", weight=65, details="", user=valid_user
        )
        test_session.add(profile)
        test_session.commit()

    test_session.rollback()


def test_profile_missing_weight(test_session, valid_user):
    # Criar perfil sem peso
    with pytest.raises(TypeError):
        profile = Profile(
            user_id=valid_user.id, name="Teste",
            birth_date=datetime(1995, 5, 15), gender="Feminino",
            details="", user=valid_user
        )
        test_session.add(profile)
        test_session.commit()

    test_session.rollback()


def test_user_with_profiles(test_session, valid_user, profile):
    """Testa associar múltiplos perfis a um usuário."""
    # Cria perfis associados ao usuário
    profile1 = profile
    profile2 = Profile(
        user_id=valid_user.id, name="Miguel",
        birth_date=datetime(2015, 6, 10), gender="Masculino",
        weight=30, details="Filho", user=valid_user
    )
    test_session.add_all([profile1, profile2])
    test_session.commit()

    # Recupera o usuário e verifica os perfis associados
    user = test_session.query(User).filter_by(id=valid_user.id).first()
    assert len(user.profiles) == 2
    assert user.profiles[0].name == "Felipe"
    assert user.profiles[1].name == "Miguel"


def test_water_intake_creation(test_session, profile):
    """Testa a criação de um registro de ingestão de água."""
    # Cria um registro de ingestão de água
    water_intake = WaterIntake(
        profile_id=profile.id,
        date=datetime(2023, 10, 1),
        amount=500.0,
        profile=profile
    )
    test_session.add(water_intake)
    test_session.commit()

    # Verifica se o registro foi salvo corretamente
    stored_intake = test_session.query(WaterIntake).filter_by(
        profile_id=profile.id).first()
    assert stored_intake is not None
    assert stored_intake.amount == 500.0
    assert stored_intake.date == datetime(2023, 10, 1)


def test_water_intake_profile_association(test_session, profile):
    """Testa a associação de um registro de ingestão de água com um usuário."""
    # Cria um registro de ingestão de água
    water_intake = WaterIntake(
        profile_id=profile.id,
        date=datetime(2023, 10, 1),
        amount=500.0,
        profile=profile
    )
    test_session.add(water_intake)
    test_session.commit()

    # Verifica se o registro está associado ao usuário correto
    pro_file = test_session.query(Profile).filter_by(id=profile.id).first()
    assert len(pro_file.water_intakes) == 1
    assert pro_file.water_intakes[0].amount == 500.0


def test_multiple_water_intakes(test_session, profile):
    """Testa a criação de múltiplos registros de ingestão de água
    para um usuário."""
    # Cria dois registros de ingestão de água
    water_intake1 = WaterIntake(
        profile_id=profile.id,
        date=datetime(2023, 10, 1),
        amount=500.0,
        profile=profile
    )
    water_intake2 = WaterIntake(
        profile_id=profile.id,
        date=datetime(2023, 10, 2),
        amount=1000.0,
        profile=profile
    )
    test_session.add(water_intake1)
    test_session.add(water_intake2)
    test_session.commit()

    # Verifica se os registros foram salvos e associados ao usuário
    water_intakes = test_session.query(WaterIntake).filter_by(
        profile_id=profile.id).all()
    assert len(water_intakes) == 2
    assert water_intakes[0].amount == 500.0
    assert water_intakes[1].amount == 1000.0


def test_water_intake_negative_amount(test_session, profile):
    """Testa se um valor negativo para amount lança uma exceção."""
    with pytest.raises(ValueError):
        water_intake = WaterIntake(
            profile_id=profile.id,
            date=datetime(2023, 10, 1),
            amount=-500.0,  # Valor negativo deve lançar uma exceção
            profile=profile
        )
        test_session.add(water_intake)
        test_session.commit()


def test_water_intake_positive_amount(test_session, profile):
    """Testa a criação de um registro de ingestão de água com valor positivo."""
    water_intake = WaterIntake(
        profile_id=profile.id,
        date=datetime(2023, 10, 1),
        profile=profile,
        amount=500.0  # Valor positivo deve ser aceito
    )
    test_session.add(water_intake)
    test_session.commit()

    # Verifica se o registro foi salvo corretamente
    stored_intake = test_session.query(WaterIntake).filter_by(
        profile_id=profile.id).first()
    assert stored_intake is not None
    assert stored_intake.amount == 500.0


def test_water_intake_deletion(test_session, profile):
    """Testa a exclusão de um registro de ingestão de água."""
    water_intake = WaterIntake(
        profile_id=profile.id,
        date=datetime(2023, 10, 1),
        amount=500.0,
        profile=profile
    )
    test_session.add(water_intake)
    test_session.commit()

    # Exclui o registro
    test_session.delete(water_intake)
    test_session.commit()

    # Verifica se o registro foi excluído
    stored_intake = test_session.query(WaterIntake).filter_by(profile_id=profile.id).first()
    assert stored_intake is None


def test_user_deletion_cascade(test_session, valid_user):
    """Testa se a deleção de um usuário remove seus perfis."""
    
    # Criar e salvar um perfil associado ao usuário
    profile = Profile(
        user_id=valid_user.id, name="Teste",
        birth_date=datetime(1995, 5, 15), gender="Feminino",
        weight=65, details="", user=valid_user
    )
    test_session.add(profile)
    test_session.commit()

    # Verificar se o perfil foi salvo corretamente
    assert test_session.query(Profile).filter_by(user_id=valid_user.id).count() == 1

    # Deletar o usuário
    test_session.delete(valid_user)
    test_session.commit()

    # Verificar se o perfil foi removido junto com o usuário
    remaining_profiles = test_session.query(Profile).filter_by(user_id=valid_user.id).all()
    assert len(remaining_profiles) == 0  # Perfis devem ser removidos


def test_delete_profile_cascade(test_session, profile):
    """Testa se a deleção de um perfil remove os registros de ingestão de água."""
    
    # Criar um registro de ingestão de água associado ao perfil
    water_intake = WaterIntake(
        profile_id=profile.id, date=datetime(2024, 1, 1),
        amount=500.0, profile=profile
    )
    test_session.add(water_intake)
    test_session.commit()

    # Verificar se o registro foi salvo corretamente
    assert test_session.query(WaterIntake).filter_by(profile_id=profile.id).count() == 1

    # Deletar o perfil
    test_session.delete(profile)
    test_session.commit()

    # Verificar se os registros de ingestão foram removidos
    remaining_intakes = test_session.query(WaterIntake).filter_by(profile_id=profile.id).all()
    assert len(remaining_intakes) == 0

    # Verificar se o perfil foi realmente deletado
    deleted_profile = test_session.query(Profile).filter_by(id=profile.id).first()
    assert deleted_profile is None


def test_update_user_email(test_session, valid_user):
    """Testa se a atualização do e-mail do usuário é persistida no banco."""
    valid_user.email = "new_email@mail.com"
    test_session.commit()

    updated_user = test_session.query(User).filter_by(id=valid_user.id).first()
    assert updated_user.email == "new_email@mail.com"


def test_update_profile_weight(test_session, profile):
    """Testa se a atualização do peso do perfil é salva corretamente."""
    profile.update_weight(75)
    test_session.add(profile)
    test_session.commit()

    updated_profile = test_session.query(Profile).filter_by(id=profile.id).first()
    assert updated_profile is not None, "O perfil não foi encontrado após a atualização!"
    assert updated_profile.weight == 75

    # Testar peso inválido
    with pytest.raises(ValueError):
        profile.update_weight(-10)