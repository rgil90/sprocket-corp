from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db_connection import Base
from app.models.utils import BaseModelMixin


class Factory(Base, BaseModelMixin):
    __tablename__ = "factories"
    name = Column(String, nullable=True)
    location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False,
    )
    sprocket_production_goal = Column(Integer, nullable=False, default=0)
    location = relationship(
        "Location",
        back_populates="factories",
        uselist=False,
    )
    sprockets = relationship("Sprocket", back_populates="factory")
    histories = relationship(
        "FactoryHistory",
        back_populates="factory",
        uselist=True,
        order_by="desc(FactoryHistory.id)",
    )

    @property
    def sprocket_production_actual(self) -> int:
        return len(self.sprockets)
