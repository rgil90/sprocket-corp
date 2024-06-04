from app.crud_services.base_crud import BaseCRUD
from app.models import Sprocket


class SprocketCRUDService(BaseCRUD):
    def _get_model(self):
        return Sprocket
