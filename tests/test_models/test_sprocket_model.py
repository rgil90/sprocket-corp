def test_sprocket_table_exists(db_inspector):
    assert db_inspector.has_table("sprockets")


def test_can_create_sprocket(mock_sprocket):
    assert mock_sprocket.id is not None
