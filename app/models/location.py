from sqlalchemy import Column, Integer

from app.db_connection import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    