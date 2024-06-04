from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db_connection import Base
from app.models.utils import BaseModelMixin


class Sprocket(BaseModelMixin, Base):
    __tablename__ = "sprockets"

    name = Column(String, nullable=False)
    sprocket_type_id = Column(
        Integer,
        ForeignKey("sprocket_types.id"),
        nullable=False,
    )
    factory_id = Column(
        Integer,
        ForeignKey("factories.id"),
        nullable=False,
    )
    sprocket_type = relationship("SprocketType", back_populates="sprockets")
    factory = relationship("Factory", back_populates="sprockets")
