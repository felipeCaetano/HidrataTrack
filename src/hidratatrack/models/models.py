from datetime import datetime

from sqlalchemy import DateTime, create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt


Base = declarative_base()

# Configuração do banco de dados
DATABASE_URL = "sqlite:///hydratrack.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Tabelas
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column('password', String(128), nullable=False)  # Bcrypt hashes are longer than SHA-256
    password_changed_at = Column(DateTime, default=datetime.utcnow)
    failed_login_attempts = Column(Integer, default=0)
    last_failed_login = Column(DateTime)
    profiles = relationship("Profile", back_populates="user", uselist=False)

    BCRYPT_WORK_FACTOR = 12

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    weight = Column(Float, nullable=False)
    details = Column(String, nullable=True)
    user = relationship("User", back_populates="profiles")

class WaterIntake(Base):
    __tablename__ = 'water_intakes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)

# Criar as tabelas
Base.metadata.create_all(engine)
