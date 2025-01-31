from models.models import session, User
from services.events import EventEmitter
from sqlalchemy.orm import Session
from models.security import hash_password

user_events = EventEmitter()

def create_user(name, email, password):
    if not all([name, email, password]):
        user_events.emit("User-warning","Por favor, preencha todos os campos.")
        return
    hashed_password = hash_password(password)
    user = User(name, email, hashed_password)
    return user


def get_user(identifier, session: Session):
    """Busca um usuário pelo e-mail ou login.

        :param identifier: Pode ser um e-mail ou um login.
        :param session: Sessão do SQLAlchemy.
        :return: Usuário encontrado ou None."""

    user_db = session.query(User).filter(
        (User.email == identifier) | (User.login == identifier)).first()

    return user_db


def save_user(user: User):
    """Salva um usuário no banco de dados.

    :param user: Objeto do tipo User
    :return: Usuário criado.
    """
    existing_user = session.query(User).filter_by(login=user.login).first()
    if existing_user:
        user_events.emit("User-warning",
            f"Usuário {user.login} já existe.")
        return existing_user
    session.add(user)
    session.commit()
    user_events.emit("User-events",
                     f"Usuário {user.login} salvo com sucesso.")
    return user