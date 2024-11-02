from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: uuid4())
    feedback: Mapped[str]
    informativeness: Mapped[float]
    objectivity: Mapped[float]
    reviewer_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    under_reviewer_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)

    reviewer = relationship("User", back_populates="sent_feedback", foreign_keys="reviewer_id", lazy="selectin")
    under_reviewer = relationship("User", back_populates="get_feedback", lazy="selectin")
    scores = relationship("Score", secondary="feedbacks_scores", back_populates="feedbacks")
