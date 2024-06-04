from tests.factories import LocationFactory


def test_can_create_new_location(db_session, client):
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
    assert response.status_code == 201


def test_can_retrieve_all_locations(db_session, client):
    location_factory = LocationFactory.build()
    location_data = {
        "address_1": location_factory.address_1,
        "address_2": location_factory.address_2,
        "city": location_factory.city,
        "state": location_factory.state,
        "country_code": location_factory.country_code,
        "postal_code": location_factory.postal_code,
    }
    client.post("/v1/locations", json=location_data)
    response = client.get("/v1/locations")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_can_retrieve_location_by_id(
    db_session,
    client,
):
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
    location_id = response.json()["id"]
    response = client.get(f"/v1/locations/{location_id}")
    assert response.status_code == 200


def test_can_retrieve_location_by_postal_code(
    db_session,
    client,
):
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
    postal_code = response.json()["postal_code"]
    response = client.get(f"/v1/locations/postal_code/{postal_code}")
    assert response.status_code == 200


def test_can_update_location(
    db_session,
    client,
):
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
    location_id = response.json()["id"]
    new_location_data = {
        "address_1": "new address",
    }
    response = client.patch(f"/v1/locations/{location_id}", json=new_location_data)
    assert response.status_code == 200
    assert response.json()["address_1"] == new_location_data["address_1"]


def test_cannot_update_location_if_location_not_found(
    db_session,
    client,
):
    response = client.patch("/v1/locations/0", json={})
    assert response.status_code == 404
