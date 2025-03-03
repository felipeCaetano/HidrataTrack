from models.models import Profile, User  # NoQA
from services.database import get_session  # NoQA
from services.events import EventEmitter  # NoQA
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

events = EventEmitter()


def create_profile(user: User, profile_name, date_obj, gender, weight, details):
    profile = Profile(
        user_id=user.id,
        name=profile_name,
        gender=gender,
        birth_date=date_obj,
        weight=weight,
        details=details,
    )
    with get_session() as session:
        existing_profile = get_profile_byid(profile.id, session)
        if existing_profile:
            events.emit("profile-warning", f"Perfil {profile.name} já existe.")
            return existing_profile
        session.add(profile)
        # profile.user = user
        # user.profiles.append(profile)
        session.commit()
        session.refresh(profile)
        events.emit("profile-event", f"Perfil {profile.name} salvo com sucesso.")
        return profile


def get_profile_byname(profile_name, session):
    existing_profile = session.query(Profile).filter_by(name=profile_name).first()
    return existing_profile


def get_profile_byid(profile_id, session):
    existing_profile = session.query(Profile).filter_by(id=profile_id).first()
    return existing_profile


def update_profile(profile, *args):
    with get_session() as session:
        try:
            session.add(profile)
            session.commit()
            events.emit("profile-event", f"Perfil {profile.name} salvo com sucesso.")
        except IntegrityError:
            events.emit("profile-warning", f"Erro ao salvar")


def update_bottle_volume(session: Session, profile_id: int, bottle_volume: float):
    profile = session.query(Profile).filter(Profile.id == profile_id).first()
    if profile:
        profile.bottle_volume = bottle_volume
        session.commit()
    else:
        events.emit("profile-warning", f"O Perfil não existe.")
