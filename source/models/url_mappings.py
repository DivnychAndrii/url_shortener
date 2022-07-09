from sqlalchemy import Column, Integer, String

from .base import Base


class UrlMappingsModel(Base):
    __tablename__ = "url_mappings"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    original_url = Column(String, nullable=False, unique=True)
    short_url = Column(String, nullable=False, unique=True)

