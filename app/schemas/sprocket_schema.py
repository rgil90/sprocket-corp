from typing import Optional
from pydantic import BaseModel


class SprocketResponseSchema(BaseModel):
    id: int
    name: str
    sprocket_type_id: int
    factory_id: int
    created_at: int
    updated_at: int


class SprocketCreateRequestSchema(BaseModel):
    name: str
    sprocket_type_id: int
    factory_id: int


class SprocketUpdateRequestSchema(BaseModel):
    name: Optional[str] = None
    sprocket_type_id: Optional[int] = None
    factory_id: Optional[int] = None
