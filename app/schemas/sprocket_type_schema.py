from typing import Optional
from pydantic import BaseModel


class SprocketTypeResponseSchema(BaseModel):
    id: int
    teeth: int
    pitch_diameter: int
    pitch: int
    outside_diameter: int
    created_at: int
    updated_at: int


class SprocketTypeCreateRequestSchema(BaseModel):
    teeth: int
    pitch_diameter: int
    pitch: int
    outside_diameter: int


class SprocketTypeUpdateRequestSchema(BaseModel):
    teeth: Optional[int] = None
    pitch_diameter: Optional[int] = None
    pitch: Optional[int] = None
    outside_diameter: Optional[int] = None


class SprocketTypeDeleteRequestSchema(BaseModel):
    id: int
