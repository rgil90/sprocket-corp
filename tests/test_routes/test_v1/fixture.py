import pytest

from tests.factories import (
    LocationFactory,
    SprocketTypeFactory,
    FactoryModelFactory,
    SprocketModelFactory,
)


@pytest.fixture(scope="function")
def location_fixture(db_session, client):
    location_factory = LocationFactory.build()
    location_data = {
        "address_1": location_factory.address_1,
        "address_2": location_factory.address_2,
        "city": location_factory.city,
        "state": location_factory.state,
        "country_code": location_factory.country_code,
        "postal_code": location_factory.postal_code,
    }
    response = client.post("/v1/locations", json=location_data)
    return response.json()


@pytest.fixture(scope="function")
def sprocket_type_fixture(db_session, client):
    sprocket_type_factory = SprocketTypeFactory.build()
    sprocket_type_data = {
        "teeth": sprocket_type_factory.teeth,
        "pitch_diameter": sprocket_type_factory.pitch_diameter,
        "pitch": sprocket_type_factory.pitch,
        "outside_diameter": sprocket_type_factory.outside_diameter,
    }
    response = client.post("/v1/sprocket_types", json=sprocket_type_data)
    return response.json()


@pytest.fixture(scope="function")
def factory_fixture(db_session, client, location_fixture):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    response = client.post("/v1/factories", json=factory_data)
    return response.json()


@pytest.fixture(scope="function")
def sprocket_fixture(db_session, client, sprocket_type_fixture, factory_fixture):
    sprocket_factory = SprocketModelFactory.build()
    sprocket_data = {
        "name": sprocket_factory.name,
        "sprocket_type_id": sprocket_type_fixture["id"],
        "factory_id": factory_fixture["id"],
    }
    response = client.post("/v1/sprockets", json=sprocket_data)
    return response.json()
