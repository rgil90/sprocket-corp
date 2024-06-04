from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError

from app.crud_services.location_crud_service import LocationCRUDService
from app.db_connection import get_db_session
from app.schemas import (
    LocationResponseSchema,
    LocationCreateRequestSchema,
    LocationUpdateRequestSchema,
)
from fastapi_pagination import paginate, Page


BASE_PATH = "/locations"

location_router = APIRouter(prefix=BASE_PATH)


def get_location_crud_service(db_session=Depends(get_db_session)):
    return LocationCRUDService(db_session=db_session)


@location_router.get(
    "",
    response_model=Page[LocationResponseSchema],
    status_code=HTTPStatus.OK.value,
)
async def get_all_locations(
    location_crud_service: LocationCRUDService = Depends(
        get_location_crud_service,
    ),
) -> Page[LocationResponseSchema]:
    return paginate(location_crud_service.list_objects())


@location_router.post(
    "",
    response_model=LocationResponseSchema,
    status_code=HTTPStatus.CREATED.value,
)
async def create_location(
    location: LocationCreateRequestSchema,
    location_crud_service: LocationCRUDService = Depends(
        get_location_crud_service,
    ),
) -> LocationResponseSchema:
    try:
        new_location = location_crud_service.create(**location.model_dump())
        db_session = location_crud_service.db_session
        db_session.commit()
        db_session.refresh(new_location)
        return new_location
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to create location",
        )


@location_router.get(
    "/{location_id}",
    response_model=LocationResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def get_location(
    location_id: int,
    location_crud_service: LocationCRUDService = Depends(
        get_location_crud_service,
    ),
) -> LocationResponseSchema:
    location = location_crud_service.get_object(location_id)
    if location is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Location not found",
        )
    return location


@location_router.get(
    "/postal_code/{postal_code}",
    response_model=LocationResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def get_location_by_postal_code(
    postal_code: str,
    location_crud_service: LocationCRUDService = Depends(
        get_location_crud_service,
    ),
) -> LocationResponseSchema:
    location = location_crud_service.get_location_by_postal_code(postal_code)
    if location is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Location not found",
        )
    return location


@location_router.patch(
    "/{location_id}",
    response_model=LocationResponseSchema,
    status_code=HTTPStatus.OK.value,
)
async def update_location(
    location_id: int,
    location: LocationUpdateRequestSchema,
    location_crud_service: LocationCRUDService = Depends(
        get_location_crud_service,
    ),
) -> LocationResponseSchema:
    if not location_crud_service.does_exist(location_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Location not found",
        )
    try:
        location_crud_service.update(location_id, location)
        db_session = location_crud_service.db_session
        db_session.commit()
        updated_location = location_crud_service.get_object(location_id)
        return updated_location
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail=error,
        )
