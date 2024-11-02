import flet as ft
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

from flet_core import ImageFit

import front.url_params as rtg

def employee_view(page):
    # Получаем параметр из URL
    user_id = rtg.get_param(page.route, "param")

    # Each attribute we'll plot in the radar chart.
    labels = ['Профессионализм', 'Командная работа', 'Коммуникабельность', 'Инициативность']

    # Number of variables we're plotting.
    num_vars = len(labels)

    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Создаем диаграмму в основном потоке
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    values = [5, 5, 1, 3]

    ax.plot(angles + [angles[0]], values + [values[0]], '#1aaf6c', linewidth=1)
    ax.fill(angles, values, '#1aaf6c', alpha=0.25)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles), labels)

    # Go through labels and adjust alignment based on where
    # it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Ensure radar goes from 0 to 100.
    ax.set_ylim(0, 5)

    # Set position of y-labels (0-100) to be in the middle
    # of the first two axes.
    ax.set_rlabel_position(180 / num_vars)

    # Add some custom styling.
    ax.tick_params(colors='#222222')
    ax.tick_params(axis='y', labelsize=11)
    ax.grid(color='#AAAAAA')
    ax.spines['polar'].set_color('#222222')
    ax.set_facecolor('none')

    # Adjust the padding around the chart
    fig.subplots_adjust(left=0.3, right=0.7, bottom=0.3, top=0.7)

    # Сохранение диаграммы в байтовый поток
    img_bytes = BytesIO()
    fig.savefig(img_bytes, format='PNG', transparent=True)

    # Преобразование байтового потока в base64-строку
    img_b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return (
        ft.View(
            "/employee",
            [
                ft.AppBar(title=ft.Text("Сотрудник"), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.Text(f"ID сотрудника: {user_id}"),
                ft.Image(src=f"data:image/png;base64,{img_b64}", width=600, height=600, fit=ft.ImageFit.CONTAIN),
                ft.ElevatedButton("Обратно", on_click=lambda e: page.go("/")),
            ],
        )
    )