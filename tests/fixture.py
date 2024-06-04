import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.utils.database_utils import migrate_to_db


@pytest.fixture(scope="session", autouse=True)
def db_session():
    engine = create_engine(os.environ.get("TEST_DATABASE_URL"))
    with engine.begin() as connection:
        migrate_to_db("app/migrations/", "app/migrations/alembic.ini", connection)

    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    yield SessionLocal
    engine.dispose()
