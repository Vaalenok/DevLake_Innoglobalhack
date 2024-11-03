from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_ip}:{settings.db_port}/{settings.db_name}"

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
