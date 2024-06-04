from app.crud_services.base_crud import BaseCRUD
from app.models import Factory, FactoryHistory


class FactoryCRUDService(BaseCRUD):
    def _get_model(self):
        return Factory

    def get_object_with_history(self, factory_id: int) -> dict:
        """
        This method returns a factory object with its historical records.
        """
        factory = self.get_object(factory_id)
        if not factory:
            return {}

        return factory.histories

    def append_sprocket_history(self, data: dict, commit=True):
        """
        This method adds a historical record to a factory.
        """
        historical_record = FactoryHistory(
            **data,
        )
        self.db_session.add(historical_record)
        if commit:
            self.db_session.commit()
            self.db_session.refresh(historical_record)
        return historical_record
