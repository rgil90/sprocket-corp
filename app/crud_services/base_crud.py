import abc

from sqlalchemy import exists


class BaseCRUD(abc.ABC):
    def __init__(self, db_session):
        self.model = self._get_model()
        self.db_session = db_session

    def list_objects(self, *filters):
        return self.db_session.query(self.model).filter(*filters).all()

    def get_object(self, id):
        result = (
            self.db_session.query(self.model).filter(self.model.id == id).one_or_none()
        )
        return result

    def create(self, **data):
        new_entity = self.model(**data)
        self.db_session.add(new_entity)
        return new_entity

    def update(self, id, data):
        self.db_session.query(self.model).filter(self.model.id == id).update(
            data.dict(exclude_unset=True)
        )

    def does_exist(self, id):
        return self.db_session.query(exists().where(self.model.id == id)).scalar()

    def delete(self, id):
        self.db_session.query(self.model).filter(self.model.id == id).delete()

    @abc.abstractmethod
    def _get_model(self):
        """Return model to be used"""
