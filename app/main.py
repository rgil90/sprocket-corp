import logging.config

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routes.v1 import (
    location_router,
    sprocket_type_router,
    factory_router,
    sprocket_router,
)


logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sprocket Corp. API",
    version="0.1",
)


def configure_v1_routes():
    app.include_router(location_router, prefix="/v1", tags=["Location"])
    app.include_router(sprocket_type_router, prefix="/v1", tags=["Sprocket Type"])
    app.include_router(factory_router, prefix="/v1", tags=["Factory"])
    app.include_router(sprocket_router, prefix="/v1", tags=["Sprocket"])


configure_v1_routes()
add_pagination(app)
