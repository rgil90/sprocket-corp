import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import SprocketType
from tests.factories.factory_connection import session


class SprocketTypeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SprocketType
        sqlalchemy_session = session

    teeth = factory.Faker("random_int", min=1, max=100)
    pitch_diameter = factory.Faker("random_int", min=1, max=100)
    pitch = factory.Faker("random_int", min=1, max=100)
    outside_diameter = factory.Faker("random_int", min=1, max=100)
