from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import AsyncSessionLocal
from src.models.feedback import Feedback
from src.models.user import User
from src.schemas.user import UserSchema
import uuid

router = APIRouter()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/users")
async def get_all_users_async(
        db: AsyncSession = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, gt=0)
):
    subquery = (
        select(
            Feedback.under_reviewer_id,
            func.count(Feedback.id).label("feedback_count")
        )
        .group_by(Feedback.under_reviewer_id)
        .subquery()
    )

    users_query = (
        select(User)
        .join(subquery, User.id == subquery.c.under_reviewer_id)
        .order_by(subquery.c.feedback_count.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(users_query)
    users = result.scalars().all()

    total_users_result = await db.execute(select(func.count()).select_from(User))
    total_users = total_users_result.scalar_one()

    return {"data": users, "total": total_users}




@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user_by_id(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(user_id == User.id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}/reviews")
async def get_user_reviews(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback).where(user_id == Feedback.under_reviewer_id))
    feedbacks = result.scalars().all()
    return feedbacks


@router.get("/users/{user_id}/own-reviews")
async def get_user_own_reviews(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback).where(user_id == Feedback.reviewer_id))
    feedbacks = result.scalars().all()
    return feedbacks


CRITERIA_TYPE_MAP = {
    "COMMUNICATION_SKILL": uuid.UUID("1a076fc9-c3ab-4682-860e-c68256688076"),
    "PROFESSIONALISM": uuid.UUID("6a8b30c1-4c9c-4f07-af48-d1bab4a12fd4"),
    "TEAMWORK": uuid.UUID("8ff4c472-de8b-4ca5-bbbb-d021e0854672"),
    "INITIATIVE": uuid.UUID("ca915514-2cc2-4ad5-94d3-846d49edc12e")
}


@router.get("/users/{user_id}/scores")
async def get_user_scores(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Feedback)
        .where(Feedback.under_reviewer_id == user_id)
    )
    feedbacks = result.scalars().all()

    if not feedbacks:
        raise HTTPException(status_code=404, detail="Feedbacks not found")

    scores_weighted = {
        "professionalism": 0,
        "teamwork": 0,
        "communication": 0,
        "initiative": 0
    }
    weights_sum = {
        "professionalism": 0,
        "teamwork": 0,
        "communication": 0,
        "initiative": 0
    }

    for feedback in feedbacks:
        weight = feedback.informativeness + feedback.objectivity

        for score in feedback.scores:
            if score.criteria_type_id == CRITERIA_TYPE_MAP["PROFESSIONALISM"]:
                scores_weighted["professionalism"] += score.score * weight
                weights_sum["professionalism"] += weight
            elif score.criteria_type_id == CRITERIA_TYPE_MAP["TEAMWORK"]:
                scores_weighted["teamwork"] += score.score * weight
                weights_sum["teamwork"] += weight
            elif score.criteria_type_id == CRITERIA_TYPE_MAP["COMMUNICATION_SKILL"]:
                scores_weighted["communication"] += score.score * weight
                weights_sum["communication"] += weight
            elif score.criteria_type_id == CRITERIA_TYPE_MAP["INITIATIVE"]:
                scores_weighted["initiative"] += score.score * weight
                weights_sum["initiative"] += weight

    avg_scores = {
        key: (scores_weighted[key] / weights_sum[key] if weights_sum[key] > 0 else 0)
        for key in scores_weighted
    }

    return avg_scores

