import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import AsyncSessionLocal
from src.models.feedback import Feedback
from src.schemas.feedback import FeedbackSchema


router = APIRouter()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/feedbacks", response_model=list[FeedbackSchema])
async def get_feedbacks(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0)
):
    result = await db.execute(
        select(Feedback)
        .offset(skip)
        .limit(limit)
    )
    feedbacks = result.scalars().all()
    return feedbacks

@router.get("/feedbacks/{fb_id}", response_model=FeedbackSchema)
async def get_feedback_by_id(fb_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback).where(fb_id == Feedback.id))
    feedback = result.scalar_one_or_none()
    if feedback is None:
        raise HTTPException(status_code=404, detail="User not found")
    return feedback
