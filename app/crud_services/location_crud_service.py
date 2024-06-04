from app.crud_services.base_crud import BaseCRUD
from app.models import Location


class LocationCRUDService(BaseCRUD):
    def _get_model(self):
        return Location

    def get_location_by_postal_code(self, postal_code):
        return (
            self.db_session.query(self.model)
            .filter(self.model.postal_code == postal_code)
            .one_or_none()
        )
