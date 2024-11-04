from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import AsyncSessionLocal
from initial_create_db import criteria_map, convert_russian_to_enum
from src.models.criteria_type import CriteriaType
from src.models.feedback import Feedback
from src.models.feedback_score import FeedbackScore
from src.models.score import Score
from src.schemas.feedback import FeedbackSchema, FeedbackCreateSchema
import uuid

from src.servicies.ai_module_service import rating_feedback


async def get_criteria_id(db: AsyncSession,name: str) -> uuid.UUID:
    criteria = await db.execute(
        select(CriteriaType).where(name == CriteriaType.name)
    )
    return criteria.scalars().first().id


router = APIRouter()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

class FeedbackResponse(BaseModel):
    data: List[FeedbackSchema]
    total: int


@router.get("/feedbacks", response_model=FeedbackResponse)
async def get_feedbacks(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    user_id: uuid.UUID = Query(None),
):
    query = select(Feedback)
    if user_id is not None:
        query = query.where(user_id == Feedback.under_reviewer_id)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    feedbacks = result.scalars().all()

    count_query = select(func.count()).select_from(Feedback)
    if user_id is not None:
        count_query = count_query.where(user_id == Feedback.under_reviewer_id)

    total_feedbacks_result = await db.execute(count_query)
    total_feedbacks = total_feedbacks_result.scalar_one()

    return {"data": feedbacks, "total": total_feedbacks}


@router.get("/feedbacks/{fb_id}", response_model=FeedbackSchema)
async def get_feedback_by_id(fb_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback).where(fb_id == Feedback.id))
    feedback = result.scalar_one_or_none()
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.post("/feedbacks/create", response_model=FeedbackSchema)
async def create_feedback(
        feedback_data: FeedbackCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    ai_review = await rating_feedback(feedback_data.feedback)
    new_feedback = Feedback(
        id=uuid.uuid4(),
        feedback=feedback_data.feedback,
        informativeness=ai_review['информативность'],
        objectivity=ai_review['объективность'],
        reviewer_id=feedback_data.reviewer_id,
        under_reviewer_id=feedback_data.under_reviewer_id
    )

    db.add(new_feedback)

    try:
        await db.commit()
        await db.refresh(new_feedback)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not create feedback: {e}")

    # Create and link scores
    feedback_scores = []
    for key, value in ai_review.items():
        if 'балл' in key:
            criteria_name = key.rsplit(' ', 1)[0]

            score = Score(
                score=value,
                commentary=ai_review.get(f"{criteria_name} объяснение", ""),
                criteria_type_id=await get_criteria_id(db, convert_russian_to_enum(criteria_name))
            )

            db.add(score)
            await db.flush()

            feedback_score = FeedbackScore(
                score_id=score.id,
                feedback_id=new_feedback.id
            )

            feedback_scores.append(feedback_score)

    db.add_all(feedback_scores)

    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not link feedback and scores: {e}")

    # Load the scores to include them in the response
    feedback_with_scores = await db.execute(
        select(Feedback).where(new_feedback.id == Feedback.id)
    )
    feedback_with_scores = feedback_with_scores.scalars().one()

    return feedback_with_scores