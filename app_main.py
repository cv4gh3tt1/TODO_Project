import flet as ft


# Classe para criar as tarefas
class Task(ft.Column): # Herda de ft.Column para criar uma coluna de tarefas
    def __init__ (self, task_name, task_status_change, task_delete): # Inicializa a classe com os parâmetros necessários
        super().__init__()
        self.task_completed = False  # Inicializa o status da tarefa como não concluída
        self.task_name = task_name  # Nome da tarefa oriunda do textfield
        self.task_status_change = task_status_change  # Função para alterar o status da tarefa
        self.task_delete = task_delete  # Função para deletar a tarefa

        def build(self):  # Método para construir a tarefa
            self.display_task = ft.Checkbox( #
                value=False, # Inicializa o checkbox como não selecionado
                label=self.task_name, # Nome da tarefa
                on_change=self.task_status_change, # Função para alterar o status da tarefa
            )

            self.edit_name = ft.TextField(expand=True, on_submit=self.clicked) # Campo de texto para editar o nome da tarefa

            self.display_view (ft.Row( # Cria uma linha para exibir a tarefa
                controls=[

                ]),)

    def save_cliced(self, e): # # Método para salvar a tarefa clicada
        pass

# Classe para Criar o Aplicativo de tarefas
class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.controls = self.build()  # Chama o método build e adiciona os controles

    def build(self):
        self.new_task = ft.TextField(
            hint_text="Digite uma nova tarefa",
            expand=True,
            on_submit=self.add_task,
        )

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="Todas"),
                ft.Tab(text="Ativas"),
                ft.Tab(text="Concluídas"),
            ],
        )

        self.items_left = ft.Text("0 tarefas restantes")

        return [
            # Titulo do App
            ft.Row(
                [
                    ft.Text(
                        value="Tarefas",
                        size=30,
                        color=ft.colors.with_opacity(0.7, "black"),
                    )
                ],
                alignment="center",
            ),
            # Insercao das tarefas
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_task),
                ],
            ),
            # Lista de Tarefas
            ft.Column(
                controls=[
                    self.filter,  # Filtro de tarefas
                    # self.tasks,  # Placeholder para as tarefas
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Apagar tarefas concluidas".upper(),
                                on_click=self.clear_completed_tasks,
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_400,
                            ),
                        ],
                    ),
                ]
            ),
        ]

    def tabs_changed(self, e):
        self.update()
        # Atualiza a exibição com base na aba selecionada

    def add_task(self, e):  # Adiciona uma nova tarefa
        pass

    def clear_completed_tasks(self, e):
        # Limpa as tarefas concluídas
        pass


# Função principal que inicializa a página
def main(page: ft.Page):
    page.title = "Minhas Tarefas"
    page.window.width = 600
    page.window.height = 650
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
    page.theme_mode = ft.ThemeMode.LIGHT

    page.update()

    app = TodoApp()  # Cria uma instância do aplicativo de tarefas

    page.add(app)  # Adiciona o aplicativo à página


ft.app(target=main)
