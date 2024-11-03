from pydantic import BaseModel
from uuid import UUID

from src.schemas.user import UserSchema


class FeedbackSchema(BaseModel):
    id: UUID
    feedback: str
    reviewer: UserSchema
    under_reviewer: UserSchema

    class Config:
        from_attributes = True
        orm_mode = True
