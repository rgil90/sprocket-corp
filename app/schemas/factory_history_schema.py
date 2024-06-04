from typing import List

from pydantic import BaseModel


class FactoryHistoryResponseSchema(BaseModel):
    sprocket_production_actual: List[int]
    sprocket_production_goal: List[int]
    time: List[int]
