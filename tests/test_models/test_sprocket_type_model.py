def test_sprocket_types_table_exists(db_inspector):
    assert db_inspector.has_table("sprocket_types")


def test_can_create_sprocket_type(mock_sprocket_type):
    assert mock_sprocket_type.id is not None
