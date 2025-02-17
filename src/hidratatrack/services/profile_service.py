from sqlalchemy.exc import IntegrityError

from models.models import Profile, User     # NoQA
from services.database import get_session   # NoQA
from services.events import EventEmitter    # NoQA

profile_events = EventEmitter()

session = next(get_session())

def create_profile(user: User, profile_name, date_obj, gender, weight, details):
    if not all([user, profile_name, weight, gender, date_obj]):
        profile_events.emit("profile-warning",
                            "Por favor, preencha todos os campos.")
        return
    user_profile = Profile(user_id=user.id, name=profile_name, gender=gender,
                           birth_date=date_obj, weight=weight, details=details,
                           user=user)
    return user_profile


def save_profile(user, profile: Profile):

    existing_profile = get_profile_byname(profile.name)
    if existing_profile:
        profile_events.emit("profile-warning",
                            f"Perfil {profile.name} já existe.")
        return existing_profile
    session.merge(profile)
    profile.user = user
    user.profiles.append(profile)
    session.commit()
    profile_events.emit("profile-event",
                        f"Perfil {profile.name} salvo com sucesso.")
    return profile


def get_profile_byname(profile_name):
    # session = next(get_session())
    existing_profile = session.query(Profile).filter_by(
        name=profile_name).first()
    return existing_profile


def get_profile_byid(profile_id):
    # session = next(get_session())
    existing_profile = session.query(
        Profile).filter_by(id=profile_id).first()
    return existing_profile


def upadate_profile(profile, dt):
    try:
        session.add(profile)
        session.commit()
        profile_events.emit("profile-event",
                                f"Perfil {profile.name} salvo com sucesso.")
    except IntegrityError:
        profile_events.emit("profile-warning", f"Erro ao salvar")

