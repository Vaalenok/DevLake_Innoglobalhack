from pydantic import BaseModel
from uuid import UUID

from src.schemas.criteria_type import CriteriaTypeSchema


class ScoreSchema(BaseModel):
    id: UUID
    score: float
    commentary: str
    criteria_type: CriteriaTypeSchema

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
