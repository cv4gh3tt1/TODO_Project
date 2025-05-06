import flet as ft
from custom_checkbox import Checkbox


def main(page: ft.Page):
    page.title = "Lista de Tarefas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.height = 600
    page.window.min_height = 600
    page.window.width = 420
    page.window.min_width = 420
    # page.bgcolor = ft.colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.window.center()
    page.padding = ft.padding.only(top=20, left=20, right=20, bottom=20)

    def add_task(e):
        print(new_task.value)
        task_list.controls.append(Checkbox(new_task.value))
        new_task.value = ""
        page.update()
        new_task.focus()

    new_task = ft.TextField(hint_text="Insira uma tarefa...", expand=True, autofocus=True)
    new_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click=add_task,
    )

    task_list = ft.Column()

    card = ft.Column(
        width=400, controls=[
            ft.Row(controls=[new_task, new_button]), task_list,]
    )

    page.add(card)


ft.app(target=main)
