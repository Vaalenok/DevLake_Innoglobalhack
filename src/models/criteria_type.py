from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class CriteriaType(Base):
    __tablename__ = 'criteria_types'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]

    scores = relationship("Score", back_populates="criteria_type")
