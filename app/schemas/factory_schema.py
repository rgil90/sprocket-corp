from typing import Optional
from pydantic import BaseModel

from app.schemas import LocationResponseSchema, FactoryHistoryResponseSchema


class FactoryResponseSchema(BaseModel):
    id: int
    name: str
    location: LocationResponseSchema
    sprocket_production_goal: int
    sprocket_production_actual: int
    created_at: int
    updated_at: int


class FactoryResponseSchemaWithChartData(FactoryResponseSchema):
    chart_data: Optional[FactoryHistoryResponseSchema] = None


class FactoryCreateRequestSchema(BaseModel):
    name: str
    location_id: int
    sprocket_production_goal: int


class FactoryUpdateRequestSchema(BaseModel):
    name: Optional[str] = None
    location_id: Optional[int] = None
    sprocket_production_goal: Optional[int] = None
