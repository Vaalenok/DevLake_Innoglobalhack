import flet as ft

from front.views.employee import employee_view
from front.views.home import home_view

def view_pop(page):
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)

def route_change(e : ft.RouteChangeEvent):
    page = e.page
    page.views.clear()

    if page.route == "/":
        # Первый экран
        page.views.append(home_view(page))
    elif page.route.startswith("/employee"):

        page.views.append(
            employee_view(page)
        )

    page.update()
