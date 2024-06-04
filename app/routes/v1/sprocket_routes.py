from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.exc import SQLAlchemyError

from app.db_connection import get_db_session
from app.crud_services.sprocket_crud_service import SprocketCRUDService
from app.schemas import (
    SprocketResponseSchema,
    SprocketCreateRequestSchema,
    SprocketUpdateRequestSchema,
)
from app.crud_services.factory_crud_service import FactoryCRUDService
from app.routes.v1.factory_routes import get_factory_crud_service


BASE_PATH = "/sprockets"

sprocket_router = APIRouter(prefix=BASE_PATH)


def get_sprocket_crud_service(db_session=Depends(get_db_session)):
    return SprocketCRUDService(db_session=db_session)


@sprocket_router.get(
    "",
    response_model=Page[SprocketResponseSchema],
    status_code=HTTPStatus.OK.value,
)
async def get_all_sprockets(
    sprocket_crud_service: SprocketCRUDService = Depends(
        get_sprocket_crud_service,
    ),
) -> Page[SprocketResponseSchema]:
    return paginate(sprocket_crud_service.list_objects())


@sprocket_router.post(
    "",
    response_model=SprocketResponseSchema,
    status_code=HTTPStatus.CREATED.value,
)
async def create_sprocket(
    sprocket: SprocketCreateRequestSchema,
    sprocket_crud_service: SprocketCRUDService = Depends(
        get_sprocket_crud_service,
    ),
    factory_crud_service: FactoryCRUDService = Depends(
        get_factory_crud_service,
    ),
) -> SprocketResponseSchema:
    try:
        new_sprocket = sprocket_crud_service.create(**sprocket.model_dump())
        db_session = sprocket_crud_service.db_session
        db_session.commit()
        db_session.refresh(new_sprocket)
        factory = new_sprocket.factory
        factory_crud_service.append_sprocket_history(
            data={
                "factory_id": factory.id,
                "sprocket_production_goal": factory.sprocket_production_goal,
                "sprocket_production_actual": factory.sprocket_production_actual,
                "sprocket_production_timestamp": new_sprocket.created_at,
            },
        )
        return new_sprocket
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to create sprocket",
        )


@sprocket_router.get(
    "/{sprocket_id}",
    response_model=SprocketResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def get_sprocket(
    sprocket_id: int,
    sprocket_crud_service: SprocketCRUDService = Depends(
        get_sprocket_crud_service,
    ),
) -> SprocketResponseSchema:
    return sprocket_crud_service.get_object(sprocket_id)


@sprocket_router.patch(
    "/{sprocket_id}",
    response_model=SprocketResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def update_sprocket(
    sprocket_id: int,
    sprocket: SprocketUpdateRequestSchema,
    sprocket_crud_service: SprocketCRUDService = Depends(
        get_sprocket_crud_service,
    ),
) -> SprocketResponseSchema:
    if not sprocket_crud_service.does_exist(sprocket_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Sprocket not found",
        )
    try:
        sprocket_crud_service.update(sprocket_id, sprocket)
        db_session = sprocket_crud_service.db_session
        db_session.commit()
        return sprocket_crud_service.get_object(sprocket_id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to update sprocket",
        )
