from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import ForeignKey, func, event
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship


from models.security import hash_password, verify_password

table_registry = registry()


# Configuração do mapeamento e do banco de dados
class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self._observers:
            observer(*args, **kwargs)


# Classes mapeadas como dataclasses
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    _password: Mapped[str] = mapped_column('password', nullable=False)
    profiles: Mapped[List["Profile"]] = relationship(
        "Profile",
        back_populates="user",
        uselist=True,
        init=False,
        cascade="all, delete-orphan",
        default_factory=list,
        lazy="selectin"
        )
    password_changed_at: Mapped[datetime] = mapped_column(default=func.now())
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    
    BCRYPT_WORK_FACTOR = 12

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = hash_password(password)
        self.password_changed_at = datetime.now()

    def verify_password(self, password: str) -> bool:
        """Verifica se a senha fornecida corresponde à senha armazenada"""
        return verify_password(password, self._password)


@table_registry.mapped_as_dataclass
class Profile:
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    birth_date: Mapped[datetime]
    gender: Mapped[str]
    weight: Mapped[float]
    details: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="profiles")
    daily_goal: Mapped[float] = mapped_column(default=2000.0)
    water_intakes: Mapped[List["WaterIntake"]] = relationship(
        "WaterIntake", back_populates="profile", uselist=True, init=False,
        cascade="all, delete-orphan", default_factory=list)

    def get_age(self):
        """Calcula a idade do usuário conforme a data de nascimento."""
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (
                self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def calculate_goal(self):
        self.daily_goal = (float(self.weight) / 20) * 1000
        return self.daily_goal

    def update_weight(self, value):
        """Atualiza o valor do peso do usuário para value"""
        if value <= 0:
            raise ValueError("O peso deve ser maior que zero!")
        self.weight = value
        self.daily_goal = self.calculate_goal(value)
        self.notify_observers()
        return self.weight
    
    def get_daily_intake(self, date_: date = None) -> float:
        """Retorna o total de água consumido em um dia específico"""
        if date_ is None:
            date_ = date.today()
        return sum(
            intake.amount for intake in self.water_intakes
            if intake.date.date() == date_
        )
    
    def notify_observers(self):
        pass


@table_registry.mapped_as_dataclass
class WaterIntake:
    __tablename__ = 'water_intakes'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey('profiles.id'))
    date: Mapped[datetime] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    profile: Mapped["Profile"] = relationship("Profile", back_populates="water_intakes")

    def __post_init__(self):
        """Valida o valor de amount ao criar um objeto WaterIntake."""
        if self.amount <= 0:
            raise ValueError("A quantidade de água deve ser maior que zero.")

# Event Listeners para validações adicionais
@event.listens_for(Profile, 'before_insert')
@event.listens_for(Profile, 'before_update')
def validate_profile(mapper, connection, target):
    if float(target.weight) <= 0:
        raise ValueError("O peso deve ser maior que zero!")
    if target.birth_date > datetime.now():
        raise ValueError("A data de nascimento não pode ser no futuro!")
