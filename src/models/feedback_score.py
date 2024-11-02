from uuid import UUID

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base



class FeedbackScore(Base):
    __tablename__ = 'feedbacks_scores'  # Исправлено, теперь используется __tablename__

    # Поле для автоматической идентификации записи в промежуточной таблице
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Поле для связи с таблицей feedbacks
    feedback_id: Mapped[UUID] = mapped_column(ForeignKey('feedbacks.id'), nullable=False)

    # Поле для связи с таблицей scores
    score_id: Mapped[UUID] = mapped_column(ForeignKey('scores.id'), nullable=False)
