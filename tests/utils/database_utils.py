import alembic.config
import alembic.command


def migrate_to_db(script_location, alembic_ini_path, connection=None, revision="head"):
    config = alembic.config.Config(alembic_ini_path)
    if connection:
        print("Migrating to db")
        config.config_ini_section = "testdb"
        alembic.command.upgrade(config, revision)
