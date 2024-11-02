from sqlalchemy.future import select
from database import AsyncSessionLocal
from src.models.feedback import Feedback
from src.models.score import Score
from src.models.user import User


async def get_all_users():
    db = AsyncSessionLocal()
    q = select(User)
    users = await db.execute(q)
    result = users.scalars().all()
    return result


async def get_user(id):
    db = AsyncSessionLocal()
    q = select(User).where(User.id == id)
    users = await db.execute(q)
    result = users.scalars()
    return result


async def get_user_feedbacks(id):
    db = AsyncSessionLocal()
    q = select(Feedback).where(Feedback.reviewer_id == id)
    feedbacks = await db.execute(q)
    result = feedbacks.scalars().all()
    return result


async def get_user_received_feedbacks(id):
    db = AsyncSessionLocal()
    q = select(Feedback).where(Feedback.under_reviewer_id == id)
    feedbacks = await db.execute(q)
    result = feedbacks.scalars().all()
    return result


# async def get_feedback_scores(id):
#     db = AsyncSessionLocal()
#     q = select(Score).where()
