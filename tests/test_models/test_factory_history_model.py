def test_factory_history_table_exists(db_inspector):
    assert db_inspector.has_table("factories_histories")


def test_can_create_factory_history(mock_factory_history):
    assert mock_factory_history.id is not None
