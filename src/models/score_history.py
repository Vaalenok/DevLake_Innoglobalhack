from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ScoreHistory(Base):
    __tablename__ = 'score_histories'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    professionalism_score: Mapped[float] = mapped_column(Float)
    professionalism_commentary: Mapped[str] = mapped_column(String)
    teamwork_score: Mapped[float] = mapped_column(Float)
    teamwork_commentary: Mapped[str] = mapped_column(String)
    communication_skills_score: Mapped[float] = mapped_column(Float)
    communication_skills_commentary: Mapped[str] = mapped_column(String)
    initiative_score: Mapped[float] = mapped_column(Float)
    initiative_commentary: Mapped[str] = mapped_column(String)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="score_history", foreign_keys=[user_id])
