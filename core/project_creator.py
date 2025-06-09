import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
from core.utils import create_project_structure, add_to_history

# Verifica se ttkbootstrap está disponível
try:
    from ttkbootstrap import Style

    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False


class ProjectCreator:
    PROJECT_TYPES = [
        "Logística", "IA", "Finanças", "Estudo",
        "Pesquisa", "Desenvolvimento", "Marketing", "Outro"
    ]

    def __init__(self, parent_frame, config):
        self.parent = parent_frame
        self.config = config
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do usuário com estilo moderno"""
        self.frame = ttk.LabelFrame(
            self.parent,
            text="Criar Novo Projeto",
            padding=(15, 10),
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Nome do Projeto
        ttk.Label(self.frame, text="Nome do Projeto:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))

        self.project_name_entry = ttk.Entry(self.frame, width=40)
        self.project_name_entry.grid(
            row=0, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))

        # Tipo de Projeto
        ttk.Label(self.frame, text="Tipo de Projeto:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 10))

        self.project_type_combo = ttk.Combobox(
            self.frame,
            values=self.PROJECT_TYPES,
            width=37,
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.project_type_combo.grid(
            row=1, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))
        self.project_type_combo.current(0)

        # Diretório Base
        ttk.Label(self.frame, text="Diretório Base:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 10))

        self.dir_frame = ttk.Frame(self.frame)
        self.dir_frame.grid(row=2, column=1, sticky=tk.EW, pady=(0, 10))

        self.dir_entry = ttk.Entry(self.dir_frame, width=30)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.dir_entry.insert(0, self.config.get('default_dir', os.path.expanduser('~/Documents/Projects')))

        self.browse_btn = ttk.Button(
            self.dir_frame,
            text="📂",
            width=3,
            command=self.browse_directory,
            bootstyle="outline" if HAS_TTKBOOTSTRAP else None
        )
        self.browse_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Opções Adicionais
        self.create_readme_var = tk.BooleanVar(value=True)
        self.create_main_py_var = tk.BooleanVar(value=True)
        self.create_spreadsheet_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            self.frame,
            text="📝 Criar README.md",
            variable=self.create_readme_var,
            bootstyle="round-toggle" if HAS_TTKBOOTSTRAP else None
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        ttk.Checkbutton(
            self.frame,
            text="🐍 Criar main.py",
            variable=self.create_main_py_var,
            bootstyle="round-toggle" if HAS_TTKBOOTSTRAP else None
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W)

        ttk.Checkbutton(
            self.frame,
            text="📊 Criar Planilha Excel",
            variable=self.create_spreadsheet_var,
            bootstyle="round-toggle" if HAS_TTKBOOTSTRAP else None
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W)

        # Botão de Criação
        self.create_btn = ttk.Button(
            self.frame,
            text="✨ Criar Projeto",
            command=self.create_project,
            bootstyle="success" if HAS_TTKBOOTSTRAP else None
        )
        self.create_btn.grid(row=6, column=0, columnspan=2, pady=(15, 0), sticky=tk.EW)

        # Configura o redimensionamento
        self.frame.columnconfigure(1, weight=1)

    def browse_directory(self):
        """Abre um diálogo para selecionar o diretório base"""
        from tkinter import filedialog
        dir_path = filedialog.askdirectory(
            initialdir=self.dir_entry.get(),
            title="Selecione o diretório base para o projeto"
        )
        if dir_path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir_path)

    def create_project(self):
        """Cria um novo projeto com a estrutura definida"""
        project_name = self.project_name_entry.get().strip()
        project_type = self.project_type_combo.get()
        base_dir = self.dir_entry.get().strip()

        if not project_name:
            messagebox.showerror("Erro", "Por favor, insira um nome para o projeto")
            return

        if not base_dir:
            messagebox.showerror("Erro", "Por favor, selecione um diretório base")
            return

        try:
            # Cria a estrutura do projeto
            project_path = create_project_structure(
                project_name,
                project_type,
                base_dir,
                create_readme=self.create_readme_var.get(),
                create_main_py=self.create_main_py_var.get()
            )

            # Adiciona ao histórico
            add_to_history(project_name, project_path, project_type)

            # Cria planilha se solicitado
            if self.create_spreadsheet_var.get():
                self.create_initial_spreadsheet(project_path, project_name, project_type)

            messagebox.showinfo(
                "Sucesso",
                f"Projeto '{project_name}' criado com sucesso em:\n{project_path}"
            )

            # Atualiza o diretório padrão nas configurações
            self.config['default_dir'] = base_dir

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar projeto:\n{str(e)}")

    def create_initial_spreadsheet(self, project_path, project_name, project_type):
        """Cria uma planilha inicial baseada no tipo de projeto"""
        os.makedirs(os.path.join(project_path, 'planilhas'), exist_ok=True)
        spreadsheet_path = os.path.join(project_path, 'planilhas', f'controle_{project_type.lower()}.xlsx')

        # Define a estrutura da planilha baseada no tipo de projeto
        if project_type == "Finanças":
            data = {
                'Data': [],
                'Descrição': [],
                'Valor': [],
                'Categoria': [],
                'Status': []
            }
        elif project_type == "Estudo":
            data = {
                'Tópico': [],
                'Data': [],
                'Horas': [],
                'Status': [],
                'Notas': []
            }
        elif project_type == "IA":
            data = {
                'Modelo': [],
                'Dataset': [],
                'Métrica': [],
                'Acurácia': [],
                'Status': []
            }
        else:  # Estrutura genérica
            data = {
                'Item': [],
                'Descrição': [],
                'Status': [],
                'Data': [],
                'Responsável': []
            }

        # Cria o DataFrame e salva como Excel
        df = pd.DataFrame(data)
        df.to_excel(spreadsheet_path, index=False)