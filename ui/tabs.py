import tkinter as tk
from tkinter import ttk

from future.moves.tkinter import filedialog

from core.project_creator import ProjectCreator
from core.excel_generator import ExcelGenerator
from core.automation import AutomationTools
from core.pomodoro import PomodoroTimer
from core.utils import get_recent_projects
from ui.notes_tab import NotesTab


class ProjectTab:
    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)
        self.creator = ProjectCreator(self.frame, config)


class SpreadsheetTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.generator = ExcelGenerator(self.frame)


class UtilitiesTab:
    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)

        # Notebook para organizar os utilitários
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Aba de Automação
        self.automation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.automation_frame, text="Automação")
        self.automation = AutomationTools(self.automation_frame, config)

        # Aba de Pomodoro
        self.pomodoro_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pomodoro_frame, text="Pomodoro")
        self.pomodoro = PomodoroTimer(self.pomodoro_frame, config)

        # Aba de Anotações
        self.notes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.notes_frame, text="Anotações")
        self.notes = NotesTab(self.notes_frame)


class HistoryTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do histórico de projetos"""
        # Barra de ferramentas
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_btn = ttk.Button(
            toolbar,
            text="Atualizar",
            command=self.refresh_projects
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar os projetos
        self.tree = ttk.Treeview(
            self.frame,
            columns=('name', 'type', 'path', 'created_at'),
            show='headings'
        )

        self.tree.heading('name', text='Nome')
        self.tree.heading('type', text='Tipo')
        self.tree.heading('path', text='Localização')
        self.tree.heading('created_at', text='Criado em')

        self.tree.column('name', width=150)
        self.tree.column('type', width=100)
        self.tree.column('path', width=300)
        self.tree.column('created_at', width=120)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carrega os projetos iniciais
        self.refresh_projects()

    def refresh_projects(self):
        """Atualiza a lista de projetos"""
        # Limpa a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Adiciona os projetos recentes
        projects = get_recent_projects(limit=50)
        for project in projects:
            self.tree.insert(
                '',
                tk.END,
                values=(
                    project['name'],
                    project['type'],
                    project['path'],
                    project['created_at']
                )
            )


class SettingsTab:
    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)
        self.config = config
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface de configurações"""
        # Tema
        ttk.Label(self.frame, text="Tema:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))

        self.theme_var = tk.StringVar(value=self.config.get('theme', 'light'))
        self.theme_combo = ttk.Combobox(
            self.frame,
            textvariable=self.theme_var,
            values=['light', 'dark'],
            state='readonly'
        )
        self.theme_combo.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=(10, 5))

        # Diretório padrão para projetos
        ttk.Label(self.frame, text="Diretório Padrão:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        self.dir_frame = ttk.Frame(self.frame)
        self.dir_frame.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=5)

        self.dir_entry = ttk.Entry(self.dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.dir_entry.insert(0, self.config.get('default_dir', ''))

        self.browse_btn = ttk.Button(
            self.dir_frame,
            text="...",
            width=3,
            command=self.browse_directory
        )
        self.browse_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Botão de salvar
        self.save_btn = ttk.Button(
            self.frame,
            text="Salvar Configurações",
            command=self.save_settings
        )
        self.save_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Configura o redimensionamento
        self.frame.columnconfigure(1, weight=1)

    def browse_directory(self):
        """Abre um diálogo para selecionar o diretório padrão"""
        dir_path = filedialog.askdirectory(
            initialdir=self.dir_entry.get(),
            title="Selecione o diretório padrão para projetos"
        )
        if dir_path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir_path)

    def save_settings(self):
        """Salva as configurações alteradas"""
        self.config['theme'] = self.theme_var.get()
        self.config['default_dir'] = self.dir_entry.get().strip()

        # Aqui você pode adicionar código para aplicar o tema imediatamente
        # se necessário, através de um callback para a janela principal