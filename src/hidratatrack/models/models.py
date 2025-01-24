from datetime import datetime, date
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

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        """Adiciona um novo observador."""
        self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove um observador existente."""
        self._observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        """Notifica todos os observadores sobre uma mudança."""
        for observer in self._observers:
            observer(*args, **kwargs)



# Classes mapeadas como dataclasses
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    profiles: Optional[Mapped["Profile"]] = relationship(
        "Profile", back_populates="user", uselist=False, init=False)
    
    # Campos opcionais ou com valor padrão (devem vir depois)
    password_changed_at: Mapped[datetime] = mapped_column(default=func.now())
    # last_failed_login: Mapped[datetime] = mapped_column(nullable=True)
    # failed_login_attempts: Mapped[int] = mapped_column(default=0)
    
    BCRYPT_WORK_FACTOR = 12


@table_registry.mapped_as_dataclass
class Profile(Observable):
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    birth_date: Mapped[datetime]
    gender: Mapped[str]
    weight: Mapped[float]
    details: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="profiles")

    def __init__(self, *args, **kwargs):
        Observable.__init__(self)
        super(Profile, self).__init__(*args, **kwargs) 

    def get_age(self):
        """Calcula a idade do usuário conforme a data de nascimento."""
        today = date.today()
        print(f'{self.data_nascimento}')
        age = today.year - self.data_nascimento.year
        if (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day):
            age -= 1
        return age
    
    def calculate_goal(self, peso):
        return (float(peso) / 20) * 1000
    
    def update_weight(self, value):
        """Atualiza o valor do peso do usuário para value"""
        if value > 0:
            self.peso = value
            self.notify_observers()
        else:
            raise ValueError("O peso deve ser maior que zero!")
        return self.peso


@table_registry.mapped_as_dataclass
class WaterIntake:
    __tablename__ = 'water_intakes'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date: Mapped[datetime] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)


# Criar as tabelas
table_registry.metadata.create_all(engine)
