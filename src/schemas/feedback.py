from pydantic import BaseModel
from uuid import UUID

from src.schemas.score import ScoreSchema
from src.schemas.user import UserSchema


class FeedbackSchema(BaseModel):
    id: UUID
    feedback: str
    informativeness: int
    objectivity: int
    scores: list[ScoreSchema]
    reviewer: UserSchema
    under_reviewer: UserSchema

    class Config:
        from_attributes = True
        orm_mode = True
