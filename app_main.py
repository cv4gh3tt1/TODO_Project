import flet as ft

# Classe para criar as tarefas
class Task(ft.Column):
    pass


# Classe para Criar o Aplicativo de tarefas
class TodoApp(ft.Column):
    def build(self):
        self.new_task = ft.TextField(
            hint_text="Digite uma nova tarefa",
            expand=True,
            on_submit=self.add_task,
        )
    
    def add_task(self, e): # Adiciona uma nova tarefa
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

    app = TodoApp() # Cria uma instância do aplicativo de tarefas
    page.add(app) # Adiciona o aplicativo à página
    
ft.app(target=main)