import datetime
from sqlalchemy import TypeDecorator, Integer, Column, Identity


class UnixTimestamp(TypeDecorator):
    """
    This class is a custom SQLAlchemy type that stores timestamps as integers
    """

    impl = Integer

    def process_bind_param(self, value, dialect):
        if value is not None:
            return int(value.timestamp())


class BaseModelMixin:
    """The basic model all the other models should extend from"""

    __allow_unmapped__ = True
    __abstract__ = True

    id = Column(Integer, Identity(always=True), primary_key=True)
    created_at = Column(
        UnixTimestamp,
        nullable=False,
        default=datetime.datetime.now(datetime.timezone.utc),
    )
    updated_at = Column(
        UnixTimestamp,
        nullable=False,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
