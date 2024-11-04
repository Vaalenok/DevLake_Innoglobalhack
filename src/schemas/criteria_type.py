from pydantic import BaseModel
from uuid import UUID


class CriteriaTypeSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True  # Активируйте режим ORM
