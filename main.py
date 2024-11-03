import asyncio
from fastapi import FastAPI
from sqlalchemy import text
from database import engine, Base, AsyncSessionLocal
from initial_create_db import init_create_db
from src.endpoints.users import router as users_router

import src.db_interface as db
from src.models import user, feedback, criteria_type, score, feedback_score, score_history

# Создаем экземпляр FastAPI
app = FastAPI()

# Определим событие запуска для инициализации базы данных
@app.on_event("startup")
async def startup_event():
    async with AsyncSessionLocal() as session:
        async with engine.begin() as conn:
            # Создаем модели в базе данных
            await conn.run_sync(Base.metadata.create_all)

        # Проверка количества пользователей
        result = await session.execute(text("select count(*) from users"))
        user_count = result.scalar()

        # Инициализируем БД (если необходимо)
        if user_count == 0:
            await init_create_db(session)

app.include_router(users_router)


# Основной вызов для запуска FastAPI приложения
if __name__ == "__main__":
    import uvicorn
    # Запуск приложения FastAPI с использованием Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)