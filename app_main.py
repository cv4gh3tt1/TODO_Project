import flet as ft


# Classe para criar as tarefas
class Task(ft.Column):  # Herda de ft.Column para criar uma coluna de tarefas
    def __init__(
        self, task_name, task_status_change, task_delete
    ):  # Inicializa a classe com os parâmetros necessários
        super().__init__()
        self.task_completed = False  # Inicializa o status da tarefa como não concluída
        self.task_name = task_name  # Nome da tarefa oriunda do textfield
        self.task_status_change = (
            task_status_change  # Função para alterar o status da tarefa
        )
        self.task_delete = task_delete  # Função para deletar a tarefa

        def build(self):  # Método para construir a tarefa
            self.display_task = ft.Checkbox(  #
                value=False,  # Inicializa o checkbox como não selecionado
                label=self.task_name,  # Nome da tarefa
                on_change=self.task_status_change,  # Função para alterar o status da tarefa
            )

            self.edit_name = ft.TextField(
                expand=True, on_submit=self.clicked
            )  # Campo de texto para editar o nome da tarefa

            self.display_view(
                ft.Row(  # Cria uma linha para exibir a tarefa
                    controls=[
                        self.display_task,  # Checkbox para marcar a tarefa como concluída
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.CREATE_OUTLINED,  # Ícone para editar a tarefa
                                    icon_color=ft.Colors.GREEN,  # Cor do ícone
                                    tooltip="Editar tarefa",  # Dica de ferramenta ao passar o mouse
                                    on_click=self.edit_clicked,  # Função chamada ao clicar no ícone de editar
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINED,  # Ícone para deletar a tarefa
                                    icon_color=ft.Colors.RED,  # Cor do ícone
                                    tooltip="Deletar tarefa",  # Dica de ferramenta ao passar o mouse
                                    on_click=self.delete_clicked,  # Função chamada ao clicar no ícone de deletar
                                ),
                            ]
                        ),
                    ]
                ),
            )

    def save_cliced(self, e):  # # Método para salvar a tarefa clicada
        pass


# Classe para Criar o Aplicativo de tarefas
class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.controls = self.build()  # Chama o método build e adiciona os controles

    def build(self):  # Método para construir o aplicativo de tarefas
        self.new_task = ft.TextField(  # Campo de texto para inserir uma nova tarefa
            hint_text="Digite uma nova tarefa",
            expand=True,
            on_submit=self.add_task,
        )

        self.filter = ft.Tabs(  # Filtro de tarefas
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,  # Função chamada ao mudar de aba
            tabs=[  # Lista de abas para filtrar as tarefas
                ft.Tab(text="Todas"),
                ft.Tab(text="Ativas"),
                ft.Tab(text="Concluídas"),
            ],
        )

        self.items_left = ft.Text(
            "0 tarefas restantes"
        )  # Texto para mostrar o número de tarefas restantes

        return [  # Lista de controles do aplicativo
            # Cabeçalho do aplicativo
            ft.Row(
                [
                    ft.Text(
                        value="Tarefas",
                        size=30,
                        color=ft.Colors.with_opacity(0.7, "black"),
                    )
                ],
                alignment="center",
            ),
            # Insercao das tarefas
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_task
                    ),  # Botão para adicionar nova tarefa
                ],
            ),
            # Lista de Tarefas
            ft.Column(
                controls=[
                    self.filter,  # Filtro de tarefas
                    ft.Row(  # # Linha para exibir as tarefas
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Apagar tarefas concluidas".upper(),
                                on_click=self.clear_completed_tasks,
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_400,
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
