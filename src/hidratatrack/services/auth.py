import logging
from datetime import datetime

from models.models import User  # NoQA
from services.database import get_session   # NoQA
from services.events import EventEmitter  # NoQA
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.hidratatrack.models.models import Profile

auth_emitter = EventEmitter()


def authenticate_user(login, password):
        """Realiza a autenticação do usuário com tratamento de erros"""
        session = next(get_session())
            
        try:
            user = session.scalar(select(User).where(User.login == login))
            if user and user.verify_password(password):
                user.last_login = datetime.now()
                session.commit()
                profiles = session.scalars(select(Profile).where(
                    Profile.user_id==user.id)).all()
                session.close()
                return user, profiles
            else:
                logging.error("Atenção Login ou senha inválidos.")
                auth_emitter.emit("login_failed",
                                "Atenção Login ou senha inválidos.")
                return False, False

        except SQLAlchemyError as db_error:
            auth_emitter.emit(
                "database_warning",
                "Erro ao conectar com o banco de dados. Tente novamente."
                )
            logging.error(f"Erro de banco de dados: {str(db_error)}")
        except Exception as e:
            auth_emitter.emit(
                "warning","Ocorreu um erro inesperado. Tente novamente.")
            logging.error(f"Erro inesperado: {str(e)}")
