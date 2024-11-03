from pydantic import BaseModel
from uuid import UUID


class UserSchema(BaseModel):
    id: UUID
    full_name: str
    experience: int
    company: str

    class Config:
        orm_mode = True
