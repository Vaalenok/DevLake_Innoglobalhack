from pydantic import BaseModel
from uuid import UUID


class ScoreSchema(BaseModel):
    id: UUID
    score: float
    commentary: str
    criteria_type_id: UUID

    class Config:
        orm_mode = True
