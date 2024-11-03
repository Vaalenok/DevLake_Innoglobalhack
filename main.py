import asyncio
import flet as ft
import front.routing as rtg
from sqlalchemy import text
from database import engine, Base, AsyncSessionLocal
from initial_create_db import init_create_db
import src.db_interface as db
from src.models import user, feedback, criteria_type, score, feedback_score, score_history


async def init_db():
    async with AsyncSessionLocal() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        result = await session.execute(text("select count(*) from users"))
        user_count = result.scalar()

        if user_count == 0:
            await init_create_db(session)


async def main(page: ft.Page):
    page.title = "DevLake"
    await init_db()

    page.on_route_change = rtg.route_change
    page.on_view_pop = rtg.view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)