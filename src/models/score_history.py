from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ScoreHistory(Base):
    __tablename__ = 'score_histories'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    professionalism_score: Mapped[float]
    professionalism_commentary: Mapped[str]
    teamwork_score: Mapped[float]
    teamwork_commentary: Mapped[str]
    communication_skills_score: Mapped[float]
    communication_skills_commentary: Mapped[str]
    initiative_score: Mapped[float]
    initiative_commentary: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="score_history", lazy="selectin")
