from datetime import datetime
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from models.models import User
from models.security import hash_password
from services.database import get_session
from services.events import EventEmitter


auth_emitter = EventEmitter()


def authenticate_user(login, password):
        """Realiza a autenticação do usuário com tratamento de erros"""
        session = next(get_session())
            
        try:
            user = session.scalar(
                select(User).options(joinedload(User.profiles)).where(User.login==login)
                )
            if user and user.verify_password(password):
                user.last_login = datetime.now()
                session.commit()
                return user
            else:
                auth_emitter.emit("login_failed",
                                "Atenção Login ou senha inválidos.")
        except SQLAlchemyError as db_error:
            auth_emitter.emit(
                "database_warning",
                "Erro ao conectar com o banco de dados. Tente novamente."
                )
            print(f"Erro de banco de dados: {str(db_error)}")
        except Exception as e:
            auth_emitter.emit(
                "warning","Ocorreu um erro inesperado. Tente novamente.")
            print(f"Erro inesperado: {str(e)}")
