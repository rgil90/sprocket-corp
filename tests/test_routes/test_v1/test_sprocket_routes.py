from tests.factories import SprocketModelFactory, FactoryModelFactory


def test_can_create_new_sprocket(
    db_session,
    client,
    sprocket_type_fixture,
    factory_fixture,
):
    sprocket_factory = SprocketModelFactory.build()
    sprocket_data = {
        "name": sprocket_factory.name,
        "sprocket_type_id": sprocket_type_fixture["id"],
        "factory_id": factory_fixture["id"],
    }
    response = client.post("/v1/sprockets", json=sprocket_data)
    assert response.status_code == 201


def test_creates_sprocket_history_row_in_factory_when_sprocket_created(
    db_session,
    client,
    sprocket_type_fixture,
    location_fixture,
):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    factory_response = client.post("/v1/factories", json=factory_data)
    factory_id = factory_response.json()["id"]
    factory_chart_data_response = client.get(
        f"/v1/factories/{factory_id}?with_chart_data=true"
    )
    assert factory_chart_data_response.status_code == 200
    assert factory_chart_data_response.json()["id"] == factory_id
    assert (
        factory_chart_data_response.json()["chart_data"]["sprocket_production_actual"][
            0
        ]
        == 0
    )

    sprocket_factory = SprocketModelFactory.build()
    sprocket_data = {
        "name": sprocket_factory.name,
        "sprocket_type_id": sprocket_type_fixture["id"],
        "factory_id": factory_response.json()["id"],
    }
    response = client.post("/v1/sprockets", json=sprocket_data)
    assert response.status_code == 201

    response = client.get(f"/v1/factories/{factory_id}?with_chart_data=true")
    assert response.status_code == 200
    assert response.json()["chart_data"]["sprocket_production_actual"][0] == 1


def test_can_retrieve_all_sprockets(
    db_session,
    client,
    sprocket_type_fixture,
    factory_fixture,
):
    sprocket_factory = SprocketModelFactory.build()
    sprocket_data = {
        "name": sprocket_factory.name,
        "sprocket_type_id": sprocket_type_fixture["id"],
        "factory_id": factory_fixture["id"],
    }
    client.post("/v1/sprockets", json=sprocket_data)
    response = client.get("/v1/sprockets")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_can_retrieve_sprocket_by_id(
    db_session,
    client,
    sprocket_type_fixture,
    factory_fixture,
):
    sprocket_factory = SprocketModelFactory.build()
    sprocket_data = {
        "name": sprocket_factory.name,
        "sprocket_type_id": sprocket_type_fixture["id"],
        "factory_id": factory_fixture["id"],
    }
    response = client.post("/v1/sprockets", json=sprocket_data)
    sprocket_id = response.json()["id"]
    response = client.get(f"/v1/sprockets/{sprocket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sprocket_id


def test_can_update_sprocket(
    db_session,
    client,
    sprocket_fixture,
):
    updated_sprocket_data = {
        "name": "Updated Sprocket Name",
    }
    response = client.patch(
        f"/v1/sprockets/{sprocket_fixture['id']}", json=updated_sprocket_data
    )
    assert response.status_code == 200

    assert response.json()["name"] == "Updated Sprocket Name"
