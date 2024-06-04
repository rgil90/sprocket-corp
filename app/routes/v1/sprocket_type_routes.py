from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.exc import SQLAlchemyError

from app.crud_services.sprocket_type_crud_service import SprocketTypeCRUDService
from app.db_connection import get_db_session

from app.schemas import (
    SprocketTypeResponseSchema,
    SprocketTypeCreateRequestSchema,
    SprocketTypeUpdateRequestSchema,
)

BASE_PATH = "/sprocket_types"

sprocket_type_router = APIRouter(prefix=BASE_PATH)


def get_sprocket_type_crud_service(db_session=Depends(get_db_session)):
    return SprocketTypeCRUDService(db_session=db_session)


@sprocket_type_router.get(
    "",
    response_model=Page[SprocketTypeResponseSchema],
    status_code=HTTPStatus.OK.value,
)
async def get_all_sprocket_types(
    sprocket_type_crud_service: SprocketTypeCRUDService = Depends(
        get_sprocket_type_crud_service,
    ),
) -> Page[SprocketTypeResponseSchema]:
    return paginate(sprocket_type_crud_service.list_objects())


@sprocket_type_router.post(
    "",
    response_model=SprocketTypeResponseSchema,
    status_code=HTTPStatus.CREATED.value,
)
async def create_sprocket_type(
    sprocket_type: SprocketTypeCreateRequestSchema,
    sprocket_type_crud_service: SprocketTypeCRUDService = Depends(
        get_sprocket_type_crud_service,
    ),
) -> SprocketTypeResponseSchema:
    try:
        new_sprocket_type = sprocket_type_crud_service.create(
            **sprocket_type.model_dump()
        )
        db_session = sprocket_type_crud_service.db_session
        db_session.commit()
        db_session.refresh(new_sprocket_type)
        return new_sprocket_type
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to create sprocket type",
        )


@sprocket_type_router.get(
    "/{sprocket_type_id}",
    response_model=SprocketTypeResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def get_sprocket_type(
    sprocket_type_id: int,
    sprocket_type_crud_service: SprocketTypeCRUDService = Depends(
        get_sprocket_type_crud_service,
    ),
) -> SprocketTypeResponseSchema:
    sprocket_type = sprocket_type_crud_service.get_object(sprocket_type_id)
    if not sprocket_type:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Sprocket type not found",
        )
    return sprocket_type


@sprocket_type_router.patch(
    "/{sprocket_type_id}",
    response_model=SprocketTypeResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def update_sprocket_type(
    sprocket_type_id: int,
    sprocket_type: SprocketTypeUpdateRequestSchema,
    sprocket_type_crud_service: SprocketTypeCRUDService = Depends(
        get_sprocket_type_crud_service,
    ),
) -> SprocketTypeResponseSchema:
    if not sprocket_type_crud_service.does_exist(sprocket_type_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Sprocket type not found",
        )

    try:
        sprocket_type_crud_service.update(
            sprocket_type_id,
            sprocket_type,
        )
        db_session = sprocket_type_crud_service.db_session
        db_session.commit()
        updated_sprocket_type = sprocket_type_crud_service.get_object(sprocket_type_id)
        return updated_sprocket_type
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to update sprocket type",
        )
