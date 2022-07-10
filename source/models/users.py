from sqlalchemy import Column, Integer, String

from .base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    public_identifier = Column(String, nullable=False, unique=True)
