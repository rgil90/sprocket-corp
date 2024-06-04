from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db_connection import Base
from app.models.utils import BaseModelMixin


class FactoryHistory(Base, BaseModelMixin):
    """
    This class represents the history of a factory's sprocket production.
    We could make this more generic to adopt use within all models
    but for now, we'll keep it specific to factories.
    """

    __tablename__ = "factories_histories"
    factory_id = Column(
        Integer,
        ForeignKey("factories.id"),
        nullable=False,
    )
    sprocket_production_goal = Column(Integer, nullable=False)
    sprocket_production_actual = Column(Integer, nullable=False)
    sprocket_production_timestamp = Column(Integer, nullable=False)
    factory = relationship(
        "Factory",
        back_populates="histories",
        uselist=False,
    )
