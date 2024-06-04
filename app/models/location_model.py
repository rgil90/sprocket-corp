from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db_connection import Base
from app.models.utils import BaseModelMixin


class Location(Base, BaseModelMixin):
    __tablename__ = "locations"

    address_1 = Column(String, nullable=False)
    address_2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    country_code = Column(String, nullable=False)
    postal_code = Column(String, nullable=False, unique=True)

    factories = relationship("Factory", back_populates="location")
