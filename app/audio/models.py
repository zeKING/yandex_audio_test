from sqlalchemy import Column, String, ForeignKey

from app.repository.base import Base


class Audio(Base):
    filename = Column(String(255), nullable=True)
    file = Column(String(255), nullable=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return f"{self.filename}"

