def test_factories_table_exists(db_inspector):
    assert db_inspector.has_table("factories")


def test_can_create_factory(mock_factory):
    assert mock_factory.id is not None
