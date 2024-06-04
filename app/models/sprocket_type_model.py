from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.db_connection import Base
from app.models.utils import BaseModelMixin


class SprocketType(BaseModelMixin, Base):
    __tablename__ = "sprocket_types"

    teeth = Column(Integer, nullable=False)
    pitch_diameter = Column(Integer, nullable=False)
    pitch = Column(Integer, nullable=False)
    outside_diameter = Column(Integer, nullable=False)
    sprockets = relationship("Sprocket", back_populates="sprocket_type")
