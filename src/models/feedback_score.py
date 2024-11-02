from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class FeedbackScore(Base):
    __tablename__ = 'feedback_scores'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    feedback_id: Mapped[UUID] = mapped_column(ForeignKey('feedbacks.id'), nullable=False)
    score_id: Mapped[UUID] = mapped_column(ForeignKey('scores.id'), nullable=False)
