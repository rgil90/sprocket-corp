from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.crud_services.factory_crud_service import FactoryCRUDService
from app.db_connection import get_db_session
from app.routes.v1.helpers import build_factory_data
from app.schemas import (
    FactoryResponseSchema,
    FactoryCreateRequestSchema,
    FactoryUpdateRequestSchema,
    FactoryResponseSchemaWithChartData,
)
from fastapi_pagination import Page, paginate

BASE_PATH = "/factories"


factory_router = APIRouter(prefix=BASE_PATH)


def get_factory_crud_service(db_session=Depends(get_db_session)):
    return FactoryCRUDService(db_session=db_session)


@factory_router.get(
    "",
    response_model=Page[FactoryResponseSchemaWithChartData],
    status_code=HTTPStatus.OK.value,
)
async def get_all_factories(
    factory_crud_service: FactoryCRUDService = Depends(
        get_factory_crud_service,
    ),
    with_chart_data: bool = False,
) -> Page[FactoryResponseSchemaWithChartData]:
    factories = factory_crud_service.list_objects()
    return paginate(
        [
            build_factory_data(factory, include_chart_data=with_chart_data)
            for factory in factories
        ]
    )


@factory_router.post(
    "",
    response_model=FactoryResponseSchema,
    status_code=HTTPStatus.CREATED.value,
)
async def create_factory(
    factory: FactoryCreateRequestSchema,
    factory_crud_service: FactoryCRUDService = Depends(
        get_factory_crud_service,
    ),
) -> FactoryResponseSchema:
    try:
        new_factory = factory_crud_service.create(**factory.model_dump())
        db_session = factory_crud_service.db_session
        db_session.commit()
        db_session.refresh(new_factory)
        factory_crud_service.append_sprocket_history(
            {
                "factory_id": new_factory.id,
                "sprocket_production_goal": new_factory.sprocket_production_goal,
                "sprocket_production_actual": new_factory.sprocket_production_actual,
                "sprocket_production_timestamp": new_factory.created_at,
            }
        )
        return build_factory_data(new_factory)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to create factory",
        )


@factory_router.get(
    "/{factory_id}",
    response_model=FactoryResponseSchemaWithChartData,
    status_code=HTTPStatus.OK.value,
)
async def get_factory(
    factory_id: int,
    with_chart_data: bool = False,
    factory_crud_service: FactoryCRUDService = Depends(
        get_factory_crud_service,
    ),
) -> FactoryResponseSchemaWithChartData:
    factory = factory_crud_service.get_object(factory_id)
    if not factory:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Factory not found",
        )
    return build_factory_data(factory, with_chart_data)


@factory_router.patch(
    "/{factory_id}",
    response_model=FactoryResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def update_factory(
    factory_id: int,
    factory: FactoryUpdateRequestSchema,
    factory_crud_service: FactoryCRUDService = Depends(
        get_factory_crud_service,
    ),
) -> FactoryResponseSchema:
    if not factory_crud_service.does_exist(factory_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Factory not found",
        )
    try:
        factory_crud_service.update(
            factory_id,
            factory,
        )
        db_session = factory_crud_service.db_session
        db_session.commit()
        updated_factory = factory_crud_service.get_object(factory_id)
        if factory.sprocket_production_goal is not None:
            factory_crud_service.append_sprocket_history(
                {
                    "factory_id": factory_id,
                    "sprocket_production_goal": updated_factory.sprocket_production_goal,
                    "sprocket_production_actual": updated_factory.sprocket_production_actual,
                    "sprocket_production_timestamp": updated_factory.updated_at,
                }
            )
        return updated_factory
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to update factory",
        )
