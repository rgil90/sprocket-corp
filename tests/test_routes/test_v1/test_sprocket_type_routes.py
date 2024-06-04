from tests.factories import SprocketTypeFactory


def test_can_create_new_sprocket_type(db_session, client):
    sprocket_type_factory = SprocketTypeFactory.build()
    sprocket_type_data = {
        "teeth": sprocket_type_factory.teeth,
        "pitch_diameter": sprocket_type_factory.pitch_diameter,
        "pitch": sprocket_type_factory.pitch,
        "outside_diameter": sprocket_type_factory.outside_diameter,
    }
    response = client.post("/v1/sprocket_types", json=sprocket_type_data)
    assert response.status_code == 201


def test_can_retrieve_all_sprocket_types(db_session, client):
    sprocket_type_factory = SprocketTypeFactory.build()
    sprocket_type_data = {
        "teeth": sprocket_type_factory.teeth,
        "pitch_diameter": sprocket_type_factory.pitch_diameter,
        "pitch": sprocket_type_factory.pitch,
        "outside_diameter": sprocket_type_factory.outside_diameter,
    }
    client.post("/v1/sprocket_types", json=sprocket_type_data)
    response = client.get("/v1/sprocket_types")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_can_retrieve_sprocket_type_by_id(
    db_session,
    client,
):
    sprocket_type_factory = SprocketTypeFactory.build()
    sprocket_type_data = {
        "teeth": sprocket_type_factory.teeth,
        "pitch_diameter": sprocket_type_factory.pitch_diameter,
        "pitch": sprocket_type_factory.pitch,
        "outside_diameter": sprocket_type_factory.outside_diameter,
    }
    response = client.post("/v1/sprocket_types", json=sprocket_type_data)
    sprocket_type_id = response.json()["id"]
    response = client.get(f"/v1/sprocket_types/{sprocket_type_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sprocket_type_id


def test_can_update_sprocket_type(
    db_session,
    client,
):
    sprocket_type_factory = SprocketTypeFactory.build()
    sprocket_type_data = {
        "teeth": sprocket_type_factory.teeth,
        "pitch_diameter": sprocket_type_factory.pitch_diameter,
        "pitch": sprocket_type_factory.pitch,
        "outside_diameter": sprocket_type_factory.outside_diameter,
    }
    response = client.post("/v1/sprocket_types", json=sprocket_type_data)
    sprocket_type_id = response.json()["id"]
    new_teeth = 100
    new_pitch_diameter = 200
    new_pitch = 300
    new_outside_diameter = 400
    updated_sprocket_type_data = {
        "teeth": new_teeth,
        "pitch_diameter": new_pitch_diameter,
        "pitch": new_pitch,
        "outside_diameter": new_outside_diameter,
    }
    response = client.patch(
        f"/v1/sprocket_types/{sprocket_type_id}", json=updated_sprocket_type_data
    )
    assert response.status_code == 200
    assert response.json()["teeth"] == new_teeth
    assert response.json()["pitch_diameter"] == new_pitch_diameter
    assert response.json()["pitch"] == new_pitch
    assert response.json()["outside_diameter"] == new_outside_diameter


def test_cannot_update_location_if_location_not_found(
    db_session,
    client,
):
    response = client.patch("/v1/sprocket_types/0", json={})
    assert response.status_code == 404
    assert response.json()["detail"] == "Sprocket type not found"
