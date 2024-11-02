from uuid import UUID, uuid4


from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    external_id: Mapped[int]
    full_name: Mapped[str]
    experience: Mapped[int]
    company: Mapped[str]

    sent_feedback = relationship("Feedback", back_populates="reviewer", foreign_keys="[Feedback.reviewer_id]")
    get_feedback = relationship("Feedback", back_populates="under_reviewer", foreign_keys="[Feedback.under_reviewer_id]")
    score_history = relationship("ScoreHistory", back_populates="user", foreign_keys="[ScoreHistory.user_id]")

