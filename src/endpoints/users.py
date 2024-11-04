import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import AsyncSessionLocal
from src.models.feedback import Feedback
from src.models.user import User
from src.schemas.user import UserSchema


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
    result = await db.execute(
        select(User)
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()

    # Исправление для получения общего числа пользователей
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
