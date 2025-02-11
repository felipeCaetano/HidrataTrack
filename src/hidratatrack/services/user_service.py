import logging
from kivy.uix.filechooser import error
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.models import User
from services.database import get_session
from services.events import EventEmitter
from models.security import hash_password


user_events = EventEmitter()


def create_user(name, email, password):
    if not all([name, email, password]):
        user_events.emit("User-warning","Por favor, preencha todos os campos.")
        return
    hashed_password = hash_password(password)
    user = User(name, email, hashed_password)
    return user


def get_user(identifier, session: Session=get_session()):
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
    :return: Usuário criado."""
    session = next(get_session())
    try:
        existing_user = session.query(User).filter_by(
            login=user.login).first()
        if existing_user:
            user_events.emit("User-warning",
                f"Usuário {user.login} já existe.")
            return existing_user
        session.merge(user)
        session.commit()
        user_events.emit("User-events",
                        f"Usuário {user.login} salvo com sucesso.")
        return user
    except SQLAlchemyError as db_error:
        user_events.emit(
                "database_warning",
                "Erro ao conectar com o banco de dados. Tente novamente."
                )
        logging.error(f"Erro de banco de dados: {str(db_error)}")
    except Exception as e:
        user_events.emit(
                "warning","Ocorreu um erro inesperado. Tente novamente.")
        logging.error()(f"Erro inesperado: {str(e)}")
