from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base
from .users import UserModel
from .url_mappings import UrlMappingsModel


class ShortLinkClicksModel(Base):
    __tablename__ = 'short_link_clicks'
    __table_args__ = (
        UniqueConstraint('user_id', 'url_mapping_id'),
    )

    user_id = Column(Integer,
                     ForeignKey('users.id', ondelete="CASCADE"),
                     nullable=False,
                     primary_key=True)
    url_mapping_id = Column(Integer,
                            ForeignKey('url_mappings.id', ondelete="CASCADE"),
                            nullable=False,
                            primary_key=True)
    count = Column(Integer, default=0, nullable=False)

    user = relationship('UserModel',
                        foreign_keys=[user_id],
                        remote_side=[UserModel.id],
                        uselist=False)

    url_mapping = relationship('UrlMappingsModel',
                               foreign_keys=[url_mapping_id],
                               remote_side=[UrlMappingsModel.id],
                               uselist=False)
