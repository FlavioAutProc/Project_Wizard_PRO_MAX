import tkinter as tk
from tkinter import ttk
from tkinter import font
import webbrowser

try:
    from ttkbootstrap import Style

    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False


class GuideTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do guia de uso"""
        self.frame = ttk.Frame(self.parent)

        # Container principal com scrollbar
        container = ttk.Frame(self.frame)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Conteúdo do guia
        self.create_section(scrollable_frame, "📌 Criar Projetos",
                            "1. Preencha o nome do projeto\n"
                            "2. Selecione o tipo de projeto\n"
                            "3. Escolha o diretório base\n"
                            "4. Adicione pastas personalizadas se necessário\n"
                            "5. Selecione os serviços que deseja incluir\n"
                            "6. Clique em 'Criar Projeto'")

        self.create_section(scrollable_frame, "🛠️ Utilitários",
                            "Para adicionar um novo utilitário:\n"
                            "1. Vá para a aba 'Utilitários' > 'Automação'\n"
                            "2. Clique no botão '+' na seção correspondente\n"
                            "3. Preencha os detalhes do utilitário\n"
                            "4. Clique em 'Salvar'")

        self.create_section(scrollable_frame, "📝 Anotações",
                            "Para criar uma nova anotação:\n"
                            "1. Vá para a aba 'Utilitários' > 'Anotações'\n"
                            "2. Clique em '+ Nova Anotação'\n"
                            "3. Preencha título, conteúdo e tags\n"
                            "4. Clique em 'Salvar'")

        self.create_section(scrollable_frame, "⌨️ Comandos Personalizados",
                            "Para adicionar um comando:\n"
                            "1. Vá para a aba 'Utilitários' > 'Automação'\n"
                            "2. Selecione a aba 'Comandos'\n"
                            "3. Digite o comando na caixa de texto\n"
                            "4. Clique em 'Executar Comando'")

        self.create_section(scrollable_frame, "⚙️ Configurações",
                            "Para alterar as configurações:\n"
                            "1. Vá para a aba 'Configurações'\n"
                            "2. Modifique as preferências\n"
                            "3. Clique em 'Salvar Configurações'")

    def create_section(self, parent, title, content):
        """Cria uma seção do guia"""
        section_frame = ttk.Frame(parent, padding=10)
        section_frame.pack(fill="x", pady=5, padx=5)

        # Título da seção
        title_label = ttk.Label(
            section_frame,
            text=title,
            font=('Helvetica', 12, 'bold')
        )
        title_label.pack(anchor="w", pady=(0, 5))

        # Conteúdo da seção
        content_label = ttk.Label(
            section_frame,
            text=content,
            justify="left"
        )
        content_label.pack(anchor="w", padx=10)

        # Linha divisória
        ttk.Separator(section_frame, orient="horizontal").pack(fill="x", pady=5)