import flet as ft

def main(page: ft.Page):
    page.title = "Minhas Tarefas"
    page.window.width = 600
    page.window.height = 650
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(ft.Text("Minhas Tarefas", size=20, weight=ft.FontWeight.BOLD))

    page.update()

ft.app(target=main)