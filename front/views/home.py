import asyncio

import flet as ft
from  src.db_interface import get_all_users

def home_view(page):
    def update_table(e=None):
        users = asyncio.run(get_all_users())
        filtered_users = [user for user in users if search_text.value.lower() in user.full_name.lower()]
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(user.full_name)),
                    ft.DataCell(ft.Text(user.company)),
                    ft.DataCell(ft.Text(user.experience)),
                ],
                on_select_changed=lambda e, user_id=user.id: page.go(f"/employee?param={user_id}"),
            ) for user in filtered_users
        ]
        page.update()

    search_text = ft.TextField(hint_text="Поиск по ФИО", on_change=lambda e: update_table())

    columns = [
        ft.DataColumn(ft.Text("ФИО")),
        ft.DataColumn(ft.Text("Компания")),
        ft.DataColumn(ft.Text("Стаж")),
    ]

    table = ft.DataTable(
        sort_column_index=0,
        sort_ascending=True,
        columns=columns,
        rows=[],
    )

    return (
        ft.View(
            "/",
            [
                ft.AppBar(title=ft.Text("Сотрудники"), bgcolor=ft.colors.SURFACE_VARIANT),
                search_text,
                table,
            ],
        )
    )
