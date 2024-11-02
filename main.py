import asyncio

import flet as ft
import pandas as pd
from faker import Faker
import random

from sqlalchemy import text

from database import engine, Base, AsyncSessionLocal
from initial_create_db import init_create_db
from src.models import user, feedback, criteria_type, score, feedback_score, score_history
from src.models.user import User


async def init_db():
    async with AsyncSessionLocal() as db:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        result = await db.execute(text("select count(*) from users"))
        user_count = result.scalar()

        if user_count == 0:
            await init_create_db(db)



async def main(page: ft.Page):
    page.title = "DevLake"
    await init_db()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)




if __name__ == "__main__":
    asyncio.run(ft.app(target=main, view=ft.AppView.WEB_BROWSER))



