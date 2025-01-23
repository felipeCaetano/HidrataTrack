from datetime import datetime
from sqlalchemy import (
    DateTime, create_engine, Column, Integer, String, Date, ForeignKey, Float,
    func
    )
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship, sessionmaker
from typing import Optional


# Configuração do mapeamento e do banco de dados
table_registry = registry()
DATABASE_URL = "sqlite:///hydratrack.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Classes mapeadas como dataclasses
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)  # Bcrypt hashes are long
    profiles: Optional[Mapped["Profile"]] = relationship("Profile", back_populates="user", uselist=False, init=False)
    
    # Campos opcionais ou com valor padrão (devem vir depois)
    password_changed_at: Mapped[datetime] = mapped_column(default=func.now())
    # last_failed_login: Mapped[datetime] = mapped_column(nullable=True)
    # failed_login_attempts: Mapped[int] = mapped_column(default=0)
    
    BCRYPT_WORK_FACTOR = 12


@table_registry.mapped_as_dataclass
class Profile:
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    birth_date: Mapped[datetime]
    weight: Mapped[float]
    details: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="profiles")


@table_registry.mapped_as_dataclass
class WaterIntake:
    __tablename__ = 'water_intakes'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date: Mapped[datetime] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)


# Criar as tabelas
table_registry.metadata.create_all(engine)
