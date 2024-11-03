import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import AsyncSessionLocal
from src.models.score import Score
from src.schemas.score import ScoreSchema


router = APIRouter()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/scores", response_model=list[ScoreSchema])
async def get_scores(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0)
):
    result = await db.execute(
        select(Score)
        .offset(skip)
        .limit(limit)
    )
    scores = result.scalars().all()
    return scores


@router.get("/scores/{score_id}", response_model=ScoreSchema)
async def get_score_by_id(score_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Score).where(score_id == Score.id))
    score = result.scalar_one_or_none()
    if score is None:
        raise HTTPException(status_code=404, detail="User not found")
    return score
