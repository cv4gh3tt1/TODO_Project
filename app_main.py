import flet as ft


# Classe para criar as tarefas
class Task(ft.Column):
    def __init__(self, task_name_str, on_status_change_callback, on_delete_callback):
        super().__init__()
        self.task_name_initial = task_name_str
        self.on_status_change_callback = on_status_change_callback
        self.on_delete_callback = on_delete_callback
        self.task_completed = False

        self._build_controls()

    def _build_controls(self):
        self.display_task_checkbox = ft.Checkbox(
            value=self.task_completed,
            label=self.task_name_initial,
            on_change=self._handle_status_change,
        )

        self.edit_name_textfield = ft.TextField(
            expand=True, on_submit=self.save_clicked
        )

        self.display_view_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task_checkbox,
                ft.Row(
                    spacing=0,  # Ajuste para os botões ficarem mais próximos
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            icon_color=ft.Colors.GREEN,
                            tooltip="Editar tarefa",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED,
                            tooltip="Deletar tarefa",
                            on_click=self._handle_delete,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view_row = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[  # Corrigido: Controls -> controls
                self.edit_name_textfield,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Atualizar tarefa",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view_row, self.edit_view_row]

    def edit_clicked(self, e):
        self.edit_name_textfield.value = self.display_task_checkbox.label
        self.display_view_row.visible = False
        self.edit_view_row.visible = True
        self.edit_name_textfield.focus()
        self.update()

    def save_clicked(self, e):
        if self.edit_name_textfield.value:  # Evita salvar nome vazio
            self.display_task_checkbox.label = self.edit_name_textfield.value
        self.display_view_row.visible = True
        self.edit_view_row.visible = False
        self.update()

    def _handle_status_change(
        self, e
    ):  # Corrigido: satus_change -> _handle_status_change
        self.task_completed = self.display_task_checkbox.value
        self.on_status_change_callback(self)  # Chama o callback do TodoApp
        # self.update() # O Checkbox se atualiza; se houver outras mudanças visuais na Task, descomente

    def _handle_delete(self, e):  # Renomeado de delete_clicked para _handle_delete
        self.on_delete_callback(self)  # Chama o callback do TodoApp
        # Não precisa de self.update() aqui, pois a Task será removida pelo TodoApp


# Classe para Criar o Aplicativo de tarefas
class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.width = 500
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centraliza horizontalmente
        self._build_ui()
        self.update_items_left()  # Atualiza a contagem inicial

    def _build_ui(self):
        self.new_task_textfield = ft.TextField(
            hint_text="Digite uma nova tarefa",
            expand=True,
            on_submit=self.add_task_handler,
        )

        self.tasks_column = ft.Column(  # Coluna dedicada para as tarefas
            spacing=10,
            # scroll=ft.ScrollMode.ADAPTIVE # Descomente se esperar muitas tarefas
        )

        self.filter_tabs = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed_handler,
            tabs=[
                ft.Tab(text="Todas"),
                ft.Tab(text="Ativas"),
                ft.Tab(text="Concluídas"),
            ],
        )

        self.items_left_text = ft.Text("0 tarefas restantes")

        self.controls = [
            ft.Row(
                [
                    ft.Text(
                        value="Tarefas",
                        size=30,
                        color=ft.Colors.with_opacity(0.7, "black"),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task_textfield,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_task_handler
                    ),
                ],
            ),
            self.filter_tabs,
            self.tasks_column,  # Adiciona a coluna de tarefas ao layout principal
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.items_left_text,
                    ft.OutlinedButton(
                        text="Apagar tarefas concluidas".upper(),
                        on_click=self.clear_completed_tasks_handler,
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_400,
                    ),
                ],
            ),
        ]

    def tabs_changed_handler(self, e):
        self.update_task_visibility()
        self.update()

    def add_task_handler(self, e):
        task_name = self.new_task_textfield.value.strip()
        if task_name:
            task = Task(
                task_name, self.task_status_change_handler, self.task_delete_handler
            )
            self.tasks_column.controls.append(task)
            self.new_task_textfield.value = ""
            self.new_task_textfield.focus()
            self.update_task_visibility()  # Aplica o filtro atual à nova tarefa
            self.update_items_left()
            self.update()

    def clear_completed_tasks_handler(self, e):
        for task in self.tasks_column.controls[:]:  # Itera sobre uma cópia da lista
            if isinstance(task, Task) and task.task_completed:
                self.task_delete_handler(task)  # Reutiliza o handler de deleção
        # update_items_left e update são chamados por task_delete_handler

    def task_status_change_handler(self, task_instance: Task):
        self.update_task_visibility()
        self.update_items_left()
        self.update()

    def task_delete_handler(self, task_instance: Task):
        self.tasks_column.controls.remove(task_instance)
        self.update_task_visibility()  # Reaplicar filtros pode ser útil
        self.update_items_left()
        self.update()

    def update_items_left(self):
        count = 0
        for task in self.tasks_column.controls:
            if isinstance(task, Task) and not task.task_completed:
                count += 1
        self.items_left_text.value = f"{count} tarefa(s) restante(s)"
        # self.update() # O chamador fará o update principal

    def update_task_visibility(self):
        current_tab_index = self.filter_tabs.selected_index
        for task in self.tasks_column.controls:
            if isinstance(task, Task):
                task.visible = (
                    (current_tab_index == 0)  # Todas
                    or (current_tab_index == 1 and not task.task_completed)  # Ativas
                    or (current_tab_index == 2 and task.task_completed)  # Concluídas
                )
        # self.update() # O chamador fará o update principal


# Função principal que inicializa a página
def main(page: ft.Page):
    page.title = "Minhas Tarefas"
    page.window.width = 600
    page.window.height = 650
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centraliza horizontalmente
    page.vertical_alignment = ft.MainAxisAlignment.CENTER #
    page.window.center()  # Centraliza a janela na tela
    page.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE  # Permite rolagem adaptativa

    app = TodoApp()  # Cria uma instância do aplicativo de tarefas

    page.add(app)  # Adiciona o aplicativo à página


ft.app(target=main)
