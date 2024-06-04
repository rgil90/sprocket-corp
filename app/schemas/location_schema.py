from typing import Optional
from pydantic import BaseModel


class LocationResponseSchema(BaseModel):
    id: int
    address_1: str
    address_2: Optional[str] = None
    city: str
    state: Optional[str] = None
    country_code: str
    postal_code: str
    created_at: int
    updated_at: int


class LocationCreateRequestSchema(BaseModel):
    address_1: str
    address_2: Optional[str] = None
    city: str
    state: Optional[str] = None
    country_code: str
    postal_code: str


class LocationUpdateRequestSchema(BaseModel):
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country_code: Optional[str] = None
    postal_code: Optional[str] = None


class LocationDeleteRequestSchema(BaseModel):
    id: int
