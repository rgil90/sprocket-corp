from app.crud_services.base_crud import BaseCRUD
from app.models import SprocketType


class SprocketTypeCRUDService(BaseCRUD):
    def _get_model(self):
        """Return model to be used"""
        return SprocketType
