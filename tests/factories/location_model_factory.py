import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import Location
from tests.factories.factory_connection import session


class LocationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Location
        sqlalchemy_session = session

    address_1 = factory.Faker("street_address")
    city = factory.Faker("city")
    country_code = factory.Faker("country_code")
    postal_code = factory.Faker("postcode")
