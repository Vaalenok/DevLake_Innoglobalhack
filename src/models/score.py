from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Score(Base):
    __tablename__ = 'scores'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    score: Mapped[float]
    commentary: Mapped[str]
    criteria_type_id: Mapped[UUID] = mapped_column(ForeignKey('criteria_types.id'))

    feedbacks = relationship("Feedback", secondary="feedbacks_scores", back_populates="scores")
    criteria_type = relationship("CriteriaType", back_populates="scores")

