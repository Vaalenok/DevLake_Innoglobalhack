from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import AsyncSessionLocal
from src.models.user import User  # Обратите внимание, что важно импортировать модель 'User'

# Создаем роутер для пользователей
router = APIRouter()

# Зависимость для получения сессии
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Получение всех пользователей
@router.get("/users")
async def get_all_users_async(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users