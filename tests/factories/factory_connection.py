import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.environ.get("TEST_DATABASE_URL"))

session = scoped_session(sessionmaker(bind=engine))
