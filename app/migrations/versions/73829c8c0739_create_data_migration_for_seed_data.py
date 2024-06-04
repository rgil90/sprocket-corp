"""create data migration for seed data

Revision ID: 73829c8c0739
Revises: 0e9587bbbd3d
Create Date: 2024-06-04 07:39:37.459355

"""

import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "73829c8c0739"
down_revision = "0e9587bbbd3d"
branch_labels = None
depends_on = None


SPROCKET_TYPES_SEED = {
    "sprockets": [
        {
            "teeth": 5,
            "pitch_diameter": 5,
            "outside_diameter": 6,
            "pitch": 1,
            "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
        },
        {
            "teeth": 5,
            "pitch_diameter": 5,
            "outside_diameter": 6,
            "pitch": 1,
            "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
        },
        {
            "teeth": 5,
            "pitch_diameter": 5,
            "outside_diameter": 6,
            "pitch": 1,
            "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
        },
    ]
}


LOCATION_SEED = {
    "locations": [
        {
            "address_1": "123 Main St",
            "address_2": None,
            "city": "Springfield",
            "state": "IL",
            "country_code": "US",
            "postal_code": "62701",
            "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
        },
        {
            "address_1": "456 Elm St",
            "address_2": None,
            "city": "Springfield",
            "state": "IL",
            "country_code": "US",
            "postal_code": "62702",
            "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
        },
        {
            "address_1": "789 Oak St",
            "address_2": None,
            "city": "Springfield",
            "state": "IL",
            "country_code": "US",
            "postal_code": "62703",
            "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
        },
    ]
}


def upgrade() -> None:
    op.bulk_insert(
        sa.Table(
            "sprocket_types",
            sa.MetaData(),
            sa.Column("teeth", sa.Integer),
            sa.Column("pitch_diameter", sa.Integer),
            sa.Column("outside_diameter", sa.Integer),
            sa.Column("pitch", sa.Integer),
            sa.Column("created_at", sa.Integer),
            sa.Column("updated_at", sa.Integer),
        ),
        SPROCKET_TYPES_SEED["sprockets"],
    )

    op.bulk_insert(
        sa.Table(
            "locations",
            sa.MetaData(),
            sa.Column("address_1", sa.String),
            sa.Column("address_2", sa.String),
            sa.Column("city", sa.String),
            sa.Column("state", sa.String),
            sa.Column("country_code", sa.String),
            sa.Column("postal_code", sa.String),
            sa.Column("created_at", sa.Integer),
            sa.Column("updated_at", sa.Integer),
        ),
        LOCATION_SEED["locations"],
    )


def downgrade() -> None:
    pass
