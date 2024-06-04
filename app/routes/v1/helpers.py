from app.schemas import (
    FactoryResponseSchemaWithChartData,
    LocationResponseSchema,
    FactoryHistoryResponseSchema,
)


def build_factory_data(
    factory_obj,
    include_chart_data: bool = False,
) -> FactoryResponseSchemaWithChartData:
    """
    This function builds a FactoryResponseSchemaWithChartData object
    """
    response_data = {
        "id": factory_obj.id,
        "name": factory_obj.name,
        "location": LocationResponseSchema(
            id=factory_obj.location.id,
            address_1=factory_obj.location.address_1,
            address_2=factory_obj.location.address_2,
            city=factory_obj.location.city,
            state=factory_obj.location.state,
            postal_code=factory_obj.location.postal_code,
            country_code=factory_obj.location.country_code,
            created_at=factory_obj.location.created_at,
            updated_at=factory_obj.location.updated_at,
        ),
        "sprocket_production_goal": factory_obj.sprocket_production_goal,
        "sprocket_production_actual": factory_obj.sprocket_production_actual,
        "created_at": factory_obj.created_at,
        "updated_at": factory_obj.updated_at,
    }
    if include_chart_data is True:
        sprocket_production_goal_list = [
            history.sprocket_production_goal for history in factory_obj.histories
        ]
        sprocket_production_actual_list = [
            history.sprocket_production_actual for history in factory_obj.histories
        ]
        timestamp_list = [
            history.sprocket_production_timestamp for history in factory_obj.histories
        ]
        response_data["chart_data"] = FactoryHistoryResponseSchema(
            sprocket_production_goal=sprocket_production_goal_list,
            sprocket_production_actual=sprocket_production_actual_list,
            time=timestamp_list,
        )

    return FactoryResponseSchemaWithChartData(**response_data)
