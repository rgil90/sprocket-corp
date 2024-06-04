from tests.factories import FactoryModelFactory


def test_can_create_new_factory(db_session, client, location_fixture):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    response = client.post("/v1/factories", json=factory_data)
    assert response.status_code == 201


def test_creates_factory_history_row_when_factory_created(
    db_session,
    client,
    location_fixture,
):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    response = client.post("/v1/factories", json=factory_data)
    assert response.status_code == 201
    factory_id = response.json()["id"]
    response = client.get(f"/v1/factories/{factory_id}?with_chart_data=true")
    assert response.status_code == 200
    assert response.json()["id"] == factory_id
    assert response.json()["chart_data"]["sprocket_production_actual"][0] == 0


def test_can_retrieve_all_factories_without_chart_data(
    db_session,
    client,
    location_fixture,
):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
    }
    client.post("/v1/factories", json=factory_data)
    response = client.get("/v1/factories")
    assert response.status_code == 200
    assert response.json()["total"] > 0


def test_can_retrieve_all_factories_with_chart_data(
    db_session,
    client,
    location_fixture,
):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    client.post("/v1/factories", json=factory_data)
    response_with_chart_data = client.get("/v1/factories?with_chart_data=true")
    assert response_with_chart_data.status_code == 200
    assert len(response_with_chart_data.json()) > 0

    assert "chart_data" in response_with_chart_data.json()["items"][0]


def test_can_retrieve_factory_by_id_without_chart_data(
    db_session,
    client,
    location_fixture,
):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    response = client.post("/v1/factories", json=factory_data)
    factory_id = response.json()["id"]
    response = client.get(f"/v1/factories/{factory_id}")
    assert response.status_code == 200
    assert response.json()["id"] == factory_id


def test_can_retrieve_factory_by_id_with_chart_data(
    db_session,
    client,
    location_fixture,
):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    response = client.post("/v1/factories", json=factory_data)
    factory_id = response.json()["id"]
    response = client.get(f"/v1/factories/{factory_id}?with_chart_data=true")
    assert response.status_code == 200
    assert response.json()["id"] == factory_id


def test_can_update_factory_by_id(
    db_session,
    client,
    location_fixture,
):
    factory_factory = FactoryModelFactory.build()
    factory_data = {
        "name": factory_factory.name,
        "location_id": location_fixture["id"],
        "sprocket_production_goal": 10,
    }
    response = client.post("/v1/factories", json=factory_data)
    factory_id = response.json()["id"]
    new_factory_name = "New Factory Name"
    new_factory_data = {"name": new_factory_name}
    response = client.patch(f"/v1/factories/{factory_id}", json=new_factory_data)
    assert response.status_code == 200
    assert response.json()["name"] == new_factory_name
    assert response.json()["id"] == factory_id


def test_creates_history_row_when_factory_sprocket_production_goal_updated(
    db_session,
    client,
    factory_fixture,
):
    factory_id = factory_fixture["id"]
    response = client.get(f"/v1/factories/{factory_id}?with_chart_data=true")
    assert response.status_code == 200
    assert response.json()["id"] == factory_id
    assert response.json()["chart_data"]["sprocket_production_actual"][0] == 0

    new_sprocket_production_goal = 20
    new_factory_data = {"sprocket_production_goal": new_sprocket_production_goal}
    response = client.patch(f"/v1/factories/{factory_id}", json=new_factory_data)
    assert response.status_code == 200
    response = client.get(f"/v1/factories/{factory_id}?with_chart_data=true")
    assert response.status_code == 200
    assert response.json()["chart_data"]["sprocket_production_actual"][0] == 0
    assert (
        response.json()["chart_data"]["sprocket_production_goal"][0]
        == new_sprocket_production_goal
    )


def test_cannot_update_factory_if_factory_not_found(
    db_session,
    client,
):
    response = client.patch("/v1/factories/0", json={})
    assert response.status_code == 404
