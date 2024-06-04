def test_location_table_exists(db_inspector):
    assert db_inspector.has_table("locations")


def test_can_create_location(mock_location):
    assert mock_location.id is not None
