from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine, Base, AsyncSessionLocal
from initial_create_db import init_create_db
from src.endpoints.users import router as users_router
from src.endpoints.feedbacks import router as feedbacks_router
from src.models import user, feedback, criteria_type, score, feedback_score, score_history
from src.models.criteria_type import CriteriaType


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
app.include_router(feedbacks_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Основной вызов для запуска FastAPI приложения
if __name__ == "__main__":
    import uvicorn

    # Запуск приложения FastAPI с использованием Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
