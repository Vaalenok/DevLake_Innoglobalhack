import flet as ft

def home_view(page):
    global rows  # Объявляем переменную rows как глобальную

    employee_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    employee_descriptions = [
        "Опытный программист",
        "Младший аналитик",
        "Менеджер по продажам",
        "Бухгалтер",
        "Системный администратор",
        "Дизайнер интерфейсов",
        "Руководитель отдела",
        "Стажер-юрист",
        "Маркетолог",
        "Специалист по обработке данных"
    ]

    search_text = ft.TextField(hint_text="Поиск по ФИО", on_change=lambda e: update_table())

    columns = [
        ft.DataColumn(ft.Text("ФИО")),
        ft.DataColumn(ft.Text("Описание")),
    ]

    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(f"Сотрудник {emp_id}")),
                ft.DataCell(ft.Text(employee_descriptions[emp_id - 1])),
            ],
            on_select_changed=lambda e, id=emp_id: page.go(f"/employee?param={id}"),
        ) for emp_id in employee_ids
    ]

    table = ft.DataTable(
        sort_column_index=0,
        sort_ascending=True,
        columns=columns,
        rows=rows
    )

    def update_table(e=None):
        global rows
        filtered_rows = [row for row in rows if search_text.value.lower() in row.cells[0].content.value.lower()]
        table.rows = filtered_rows
        page.update()

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
