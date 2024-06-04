import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import Sprocket
from tests.factories.factory_connection import session


class SprocketModelFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Sprocket
        sqlalchemy_session = session

    name = factory.Faker("company")
    sprocket_type_id = factory.SubFactory(
        "tests.factories.sprocket_type_model_factory.SprocketTypeFactory"
    )
    factory_id = factory.SubFactory(
        "tests.factories.factory_model_factory.FactoryModelFactory"
    )
