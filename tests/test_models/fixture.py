import pytest
from sqlalchemy import inspect

from tests.factories import (
    LocationFactory,
    SprocketTypeFactory,
    FactoryModelFactory,
    FactoryHistoryModelFactory,
    SprocketModelFactory,
)


@pytest.fixture(scope="function")
def db_inspector(db_session):
    """
    This will tell us about the tables in the database
    :param db_session:
    :return:
    """
    return inspect(db_session().bind)


@pytest.fixture(scope="function")
def mock_location(db_session):
    with db_session() as session:
        location = LocationFactory.build()
        session.add(location)
        session.commit()
        session.refresh(location)
        return location


@pytest.fixture(scope="function")
def mock_sprocket_type(db_session):
    with db_session() as session:
        sprocket_type = SprocketTypeFactory.build()
        session.add(sprocket_type)
        session.commit()
        session.refresh(sprocket_type)
        return sprocket_type


@pytest.fixture(scope="function")
def mock_factory(mock_location, db_session):
    with db_session() as session:
        factory = FactoryModelFactory.build(location_id=mock_location.id)
        session.add(factory)
        session.commit()
        session.refresh(factory)
        return factory


@pytest.fixture(scope="function")
def mock_factory_history(mock_factory, db_session):
    with db_session() as session:
        factory_history = FactoryHistoryModelFactory.build(factory_id=mock_factory.id)
        session.add(factory_history)
        session.commit()
        session.refresh(factory_history)
        return factory_history


@pytest.fixture(scope="function")
def mock_sprocket(mock_sprocket_type, mock_factory, db_session):
    with db_session() as session:
        sprocket = SprocketModelFactory.build(
            factory_id=mock_factory.id,
            sprocket_type_id=mock_sprocket_type.id,
        )
        session.add(sprocket)
        session.commit()
        session.refresh(sprocket)
        return sprocket
