from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings

DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_ip}:{settings.db_port}/{settings.db_name}"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
