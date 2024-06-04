import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DEV_DATABASE = os.getenv("DEV_DATABASE_URL")

engine = create_engine(DEV_DATABASE, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def get_db_session():
    """
    This function is used to get a database session
    :return: 
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()