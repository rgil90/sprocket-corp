import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import FactoryHistory
from tests.factories.factory_connection import session


class FactoryHistoryModelFactory(SQLAlchemyModelFactory):
    class Meta:
        model = FactoryHistory
        sqlalchemy_session = session

    factory_id = factory.SubFactory(
        "tests.factories.factory_model_factory.FactoryModelFactory"
    )
    sprocket_production_goal = factory.Faker("random_int", min=1, max=100)
    sprocket_production_actual = factory.Faker("random_int", min=1, max=100)
    sprocket_production_timestamp = factory.Sequence(lambda n: n + 1)
