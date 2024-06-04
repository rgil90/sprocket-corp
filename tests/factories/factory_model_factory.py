import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import Factory
from tests.factories.factory_connection import session


class FactoryModelFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Factory
        sqlalchemy_session = session

    name = factory.Faker("company")
    location_id = factory.SubFactory(
        "tests.factories.location_model_factory.LocationFactory"
    )
    sprocket_production_goal = factory.Faker("random_int", min=1, max=100)
