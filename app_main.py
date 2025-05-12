import flet as ft


# Classe para criar as tarefas individualmente
# Cada tarefa tem um nome, status (concluída ou não) e controles para editar e deletar
class Task(ft.Column):
    def __init__(self, task_name_str, on_status_change_callback, on_delete_callback):
        super().__init__()
        self.task_name_initial = task_name_str
        self.on_status_change_callback = on_status_change_callback
        self.on_delete_callback = on_delete_callback  # Callback para deletar a tarefa
        self.task_completed = False

        # Constrói a interface inicial da tarefa
        self._build_controls()

    # Método para construir os controles da tarefa
    # Cria os elementos da interface, como checkbox, textfield e botões
    def _build_controls(self):
        # Cria o checkbox para marcar a tarefa como concluída ou não
        # O checkbox chama o método _handle_status_change quando seu valor muda
        self.display_task_checkbox = ft.Checkbox(
            value=self.task_completed,
            label=self.task_name_initial,
            on_change=self._handle_status_change,
        )
        # Cria o textfield para editar o nome da tarefa
        # O textfield chama o método save_clicked quando o usuário pressiona Enter
        self.edit_name_textfield = ft.TextField(
            expand=True, on_submit=self.save_clicked
        )
        # Cria a linha de visualização da tarefa, que contém o checkbox e os botões de editar e deletar
        # Esta linha é visível por padrão e contém o checkbox e os botões de ação
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
        # Cria a linha de edição da tarefa, que contém o textfield e o botão de salvar
        # Esta linha começa invisível e só aparece quando o usuário clica para editar a tarefa
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
        #  Adiciona as linhas de visualização e edição à coluna da tarefa
        self.controls = [self.display_view_row, self.edit_view_row]

    # Metodo para editar a tarefa
    # Torna o textfield visível e oculta a visualização normal
    def edit_clicked(self, e):
        self.edit_name_textfield.value = self.display_task_checkbox.label
        self.display_view_row.visible = False
        self.edit_view_row.visible = True
        self.edit_name_textfield.focus()
        self.update()

    # Método para salvar as alterações feitas na tarefa
    # Atualiza o nome da tarefa e volta para a visualização normal
    def save_clicked(self, e):
        if self.edit_name_textfield.value:  # Evita salvar nome vazio
            self.display_task_checkbox.label = self.edit_name_textfield.value
        self.display_view_row.visible = True
        self.edit_view_row.visible = False
        self.update()

    # Método para lidar com a mudança de status da tarefa
    # Atualiza o status da tarefa e chama o callback apropriado
    def _handle_status_change(
        self, e
    ):  # Corrigido: satus_change -> _handle_status_change
        self.task_completed = self.display_task_checkbox.value
        self.on_status_change_callback(self)  # Chama o callback do TodoApp
        # self.update() # O Checkbox se atualiza; se houver outras mudanças visuais na Task, descomente

    # Método para lidar com a exclusão da tarefa
    # Chama o callback de deleção e remove a tarefa da interface
    def _handle_delete(self, e):
        self.on_delete_callback(self)  # Chama o callback do TodoApp


# Classe para Criar o Aplicativo de tarefas
# Esta classe contém a lógica principal do aplicativo, incluindo a adição, remoção e atualização de tarefas
# Além disso, ela gerencia a interface do usuário e a interação com o usuário
class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.width = 500
        self.horizontal_alignment = (
            ft.CrossAxisAlignment.CENTER
        )  # Centraliza horizontalmente
        self._build_ui()
        self.update_items_left()  # Atualiza a contagem inicial
        self._update_clear_button_visibility()  # Define a visibilidade inicial do botão

    # Método para construir a interface do usuário
    # Cria os elementos principais, como textfield, coluna de tarefas e botões
    def _build_ui(self):

        # Cria o campo de texto para adicionar novas tarefas
        # Este campo de texto permite ao usuário digitar o nome da nova tarefa
        self.new_task_textfield = ft.TextField(
            hint_text="Digite uma nova tarefa",
            expand=True,
            border_color="BLUE_400",
            filled=True,
            fill_color="BLUE_50",
            on_submit=self.add_task_handler,
        )

        # Cria a coluna de tarefas
        # Esta coluna conterá todas as tarefas adicionadas pelo usuário
        self.tasks_column = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE,
            # auto_scroll=True,
            expand=True,
        )

        # Cria as abas para filtrar as tarefas
        # As abas permitem ao usuário ver todas as tarefas, apenas as ativas ou apenas as concluídas
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

        # Cria o texto que mostra quantas tarefas ainda restam
        # Este texto é atualizado sempre que uma tarefa é adicionada ou removida
        self.items_left_text = ft.Text("0 tarefas restantes")

        # Cria o botão para limpar tarefas concluídas
        # Este botão só aparece quando há tarefas concluídas
        self.clear_completed_button = ft.OutlinedButton(
            text="Apagar tarefas concluidas".upper(),
            on_click=self.clear_completed_tasks_handler,
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_400,
            visible=False,  # Começa oculto
        )

        # Cria o layout principal do aplicativo
        # Este layout contém todos os elementos criados acima
        self.controls = [
            # Cria uma linha para o título
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
            # Cria uma linha para o campo de texto e o botão de adicionar tarefa
            # O botão de adicionar tarefa é um botão flutuante que aparece ao lado do campo de texto
            ft.Row(
                controls=[
                    # Campo de texto para nova tarefa
                    self.new_task_textfield,
                    # Botão flutuante para adicionar tarefa
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        tooltip="Adicionar tarefa",
                        height=50,
                        width=50,
                        on_click=self.add_task_handler,
                    ),
                ],
            ),
            self.filter_tabs,  # Adiciona as abas ao layout principal
            self.tasks_column,  # Adiciona a coluna de tarefas ao layout principal
            # Cria uma linha para o texto de tarefas restantes e o botão de limpar tarefas concluídas
            # O botão de limpar tarefas concluídas só aparece quando há tarefas concluídas
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.items_left_text,
                    self.clear_completed_button,
                ],
            ),
        ]

    # Método para lidar com a mudança de abas
    # Atualiza a visibilidade das tarefas com base na aba selecionada
    def tabs_changed_handler(self, e):
        self.update_task_visibility()
        # A mudança de aba não afeta quais tarefas estão concluídas, então não precisa chamar _update_clear_button_visibility aqui
        self.update()

    # Método para adicionar uma nova tarefa
    # Cria uma instância da classe Task e a adiciona à coluna de tarefas
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
            self._update_clear_button_visibility()  # Verifica se o botão deve ser mostrado
            self.update()

    # Método para lidar com a exclusão de tarefas concluídas
    # Itera sobre as tarefas e remove as que estão concluídas
    def clear_completed_tasks_handler(self, e):
        for task in self.tasks_column.controls[:]:  # Itera sobre uma cópia da lista
            if isinstance(task, Task) and task.task_completed:
                self.task_delete_handler(task)  # Reutiliza o handler de deleção

    # Método para lidar com a mudança de status da tarefa
    # Atualiza a visibilidade das tarefas e a contagem de tarefas restantes
    def task_status_change_handler(self, task_instance: Task):
        self.update_task_visibility()
        self.update_items_left()
        self._update_clear_button_visibility()
        self.update()

    # Método para lidar com a exclusão de tarefas
    # Remove a tarefa da coluna de tarefas e atualiza a contagem de tarefas restantes
    def task_delete_handler(self, task_instance: Task):
        self.tasks_column.controls.remove(task_instance)
        self.update_task_visibility()  # Reaplicar filtros pode ser útil
        self.update_items_left()
        self._update_clear_button_visibility()
        self.update()

    # Método para atualizar o texto que mostra quantas tarefas ainda restam
    # Conta as tarefas não concluídas e atualiza o texto correspondente
    def update_items_left(self):
        count = 0
        for (
            task
        ) in (
            self.tasks_column.controls
        ):  # percorre as tarefas na coluna e conta as não concluídas
            if (
                isinstance(task, Task) and not task.task_completed
            ):  # Verifica se é uma Task e não está concluída
                count += 1
        self.items_left_text.value = f"{count} tarefa(s) restante(s)"
        # self.items_left_text.update() # Atualiza o texto na interface

    # Método para atualizar a visibilidade do botão de limpar tarefas concluídas
    # Verifica se há tarefas concluídas e atualiza a visibilidade do botão
    def _update_clear_button_visibility(self):
        any_completed = False
        for task in self.tasks_column.controls:
            if isinstance(task, Task) and task.task_completed:
                any_completed = True
                break
        self.clear_completed_button.visible = any_completed
        # A atualização da UI será feita pelo método chamador (ex: self.update() em task_status_change_handler)

    # Método para atualizar a visibilidade das tarefas com base na aba selecionada
    # Mostra ou oculta as tarefas dependendo da aba ativa (todas, ativas ou concluídas)
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


# Função principal que inicializa a página do aplicativo
# Define o título, tamanho da janela, alinhamento e tema
def main(page: ft.Page):
    page.title = "Minhas Tarefas"
    page.window.width = 600
    page.window.height = 650
    page.horizontal_alignment = (
        ft.CrossAxisAlignment.CENTER
    )  # Centraliza horizontalmente
    page.vertical_alignment = ft.MainAxisAlignment.START  #
    page.window.center()  # Centraliza a janela na tela
    page.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.scroll = ft.ScrollMode.ADAPTIVE  # Permite rolagem adaptativa

    app = TodoApp()  # Cria uma instância do aplicativo de tarefas

    app.expand = (
        True  # Permite que o aplicativo expanda para preencher o espaço disponível
    )
    page.add(app)  # Adiciona o aplicativo à página


# Executa o aplicativo com o método main
# Se o arquivo for executado diretamente, inicia o aplicativo
ft.app(target=main)
