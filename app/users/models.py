import datetime

from pydantic import create_model

from app.exceptions import ModelNotFoundException
from app.repository.base import Base
from app.database import async_session_maker
from sqlalchemy import Column, String, DateTime, ForeignKey, select, JSON, func, Boolean, UniqueConstraint, insert, \
    BigInteger, Date
from sqlalchemy.orm import joinedload, Mapped

from sqlalchemy.orm import relationship
from app.audio.models import Audio

class User(Base):

    id = Column(String(length=20), primary_key=True) # т.к. с яндекса у id тип str
    email = Column(String(length=255), nullable=False, unique=True)
    login = Column(String(length=255), nullable=True)
    first_name = Column(String(length=255), nullable=True)
    last_name = Column(String(length=255), nullable=True)
    gender = Column(String(length=255), nullable=True)  # очень хотелось Boolean, default=True сделать, но увы :)

    phone = Column(String(length=20), nullable=True)
    avatar_id = Column(String(length=255), nullable=True)
    avatar = Column(String(length=255), nullable=True)

    is_superuser = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    last_login = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    files = relationship('Audio')

    def __str__(self):
        return f"{self.email}"


