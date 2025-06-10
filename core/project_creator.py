import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
from core.utils import create_project_structure, add_to_history
import json

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

    SERVICE_TYPES = {
        "Banco de Dados": ["MySQL", "PostgreSQL", "MongoDB", "SQLite"],
        "API": ["REST", "GraphQL", "SOAP"],
        "Frontend": ["React", "Vue", "Angular", "Svelte"],
        "Backend": ["Node.js", "Django", "Flask", "FastAPI"],
        "Mobile": ["React Native", "Flutter", "Swift", "Kotlin"],
        "Cloud": ["AWS", "Azure", "Google Cloud", "Digital Ocean"]
    }

    def __init__(self, parent_frame, config):
        self.parent = parent_frame
        self.config = config
        self.custom_dirs = []
        self.selected_services = {}
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

        # Notebook para organizar as configurações
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Aba Básica
        self.basic_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_tab, text="Configurações Básicas")
        self.setup_basic_tab()

        # Aba de Estrutura
        self.structure_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.structure_tab, text="Estrutura de Pastas")
        self.setup_structure_tab()

        # Aba de Serviços
        self.services_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.services_tab, text="Serviços")
        self.setup_services_tab()

        # Botão de Criação
        self.create_btn = ttk.Button(
            self.frame,
            text="✨ Criar Projeto",
            command=self.create_project,
            bootstyle="success" if HAS_TTKBOOTSTRAP else None
        )
        self.create_btn.pack(pady=(15, 0), fill=tk.X)

    def setup_basic_tab(self):
        """Configura a aba de configurações básicas"""
        # Nome do Projeto
        ttk.Label(self.basic_tab, text="Nome do Projeto:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))

        self.project_name_entry = ttk.Entry(self.basic_tab, width=40)
        self.project_name_entry.grid(
            row=0, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))

        # Tipo de Projeto
        ttk.Label(self.basic_tab, text="Tipo de Projeto:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 10))

        self.project_type_combo = ttk.Combobox(
            self.basic_tab,
            values=self.PROJECT_TYPES,
            width=37,
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.project_type_combo.grid(
            row=1, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))
        self.project_type_combo.current(0)

        # Diretório Base
        ttk.Label(self.basic_tab, text="Diretório Base:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 10))

        self.dir_frame = ttk.Frame(self.basic_tab)
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
            self.basic_tab,
            text="📝 Criar README.md",
            variable=self.create_readme_var,
            bootstyle="round-toggle" if HAS_TTKBOOTSTRAP else None
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        ttk.Checkbutton(
            self.basic_tab,
            text="🐍 Criar main.py",
            variable=self.create_main_py_var,
            bootstyle="round-toggle" if HAS_TTKBOOTSTRAP else None
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W)

        ttk.Checkbutton(
            self.basic_tab,
            text="📊 Criar Planilha Excel",
            variable=self.create_spreadsheet_var,
            bootstyle="round-toggle" if HAS_TTKBOOTSTRAP else None
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W)

        # Configura o redimensionamento
        self.basic_tab.columnconfigure(1, weight=1)

    def setup_structure_tab(self):
        """Configura a aba de estrutura de pastas personalizada"""
        # Frame para a lista de diretórios
        self.dirs_frame = ttk.Frame(self.structure_tab)
        self.dirs_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Treeview para mostrar os diretórios
        self.dirs_tree = ttk.Treeview(
            self.dirs_frame,
            columns=('path',),
            show='tree',
            height=5
        )
        self.dirs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(
            self.dirs_frame,
            orient=tk.VERTICAL,
            command=self.dirs_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dirs_tree.configure(yscrollcommand=scrollbar.set)

        # Controles para adicionar/remover diretórios
        controls_frame = ttk.Frame(self.structure_tab)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        # Entrada para novo diretório
        self.new_dir_entry = ttk.Entry(controls_frame)
        self.new_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Botão para adicionar
        ttk.Button(
            controls_frame,
            text="+ Adicionar",
            command=self.add_custom_dir,
            bootstyle="success-outline" if HAS_TTKBOOTSTRAP else None
        ).pack(side=tk.LEFT, padx=(0, 5))

        # Botão para remover
        ttk.Button(
            controls_frame,
            text="- Remover",
            command=self.remove_custom_dir,
            bootstyle="danger-outline" if HAS_TTKBOOTSTRAP else None
        ).pack(side=tk.LEFT)

        # Adiciona diretórios padrão
        self.add_default_dirs()

    def setup_services_tab(self):
        """Configura a aba de seleção de serviços"""
        # Frame principal com scrollbar
        self.services_canvas = tk.Canvas(self.services_tab)
        self.services_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            self.services_tab,
            orient=tk.VERTICAL,
            command=self.services_canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.services_canvas.configure(yscrollcommand=scrollbar.set)
        self.services_canvas.bind(
            '<Configure>',
            lambda e: self.services_canvas.configure(
                scrollregion=self.services_canvas.bbox("all")
            )
        )

        # Frame interno para os serviços
        self.services_frame = ttk.Frame(self.services_canvas)
        self.services_canvas.create_window(
            (0, 0), window=self.services_frame, anchor="nw")

        # Cria cards para cada tipo de serviço
        for i, (service_type, options) in enumerate(self.SERVICE_TYPES.items()):
            self.create_service_card(service_type, options, i)

    def create_service_card(self, service_type, options, row):
        """Cria um card de seleção para um tipo de serviço"""
        card = ttk.LabelFrame(
            self.services_frame,
            text=service_type,
            padding=10,
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        card.grid(row=row, column=0, sticky=tk.EW, pady=5, padx=5)

        # Variável para armazenar a seleção
        var = tk.StringVar()
        self.selected_services[service_type] = var

        # Opção "Nenhum"
        ttk.Radiobutton(
            card,
            text="Nenhum",
            variable=var,
            value="",
            bootstyle="toolbutton" if HAS_TTKBOOTSTRAP else None
        ).pack(anchor=tk.W)

        # Opções específicas
        for option in options:
            ttk.Radiobutton(
                card,
                text=option,
                variable=var,
                value=option,
                bootstyle="toolbutton" if HAS_TTKBOOTSTRAP else None
            ).pack(anchor=tk.W)

    def add_default_dirs(self):
        """Adiciona diretórios padrão à árvore"""
        default_dirs = ['dados', 'documentos', 'relatorios', 'planilhas', 'scripts', 'outputs']
        for dir_name in default_dirs:
            self.dirs_tree.insert('', 'end', text=dir_name, values=(dir_name,))
            self.custom_dirs.append(dir_name)

    def add_custom_dir(self):
        """Adiciona um diretório personalizado à lista"""
        dir_name = self.new_dir_entry.get().strip()
        if dir_name and dir_name not in self.custom_dirs:
            self.dirs_tree.insert('', 'end', text=dir_name, values=(dir_name,))
            self.custom_dirs.append(dir_name)
            self.new_dir_entry.delete(0, tk.END)

    def remove_custom_dir(self):
        """Remove o diretório selecionado da lista"""
        selected = self.dirs_tree.selection()
        if selected:
            dir_name = self.dirs_tree.item(selected[0], 'text')
            self.custom_dirs.remove(dir_name)
            self.dirs_tree.delete(selected[0])

    def browse_directory(self):
        """Abre um diálogo para selecionar o diretório base"""
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
                custom_dirs=self.custom_dirs,
                create_readme=self.create_readme_var.get(),
                create_main_py=self.create_main_py_var.get(),
                services=self.get_selected_services()
            )

            # Adiciona ao histórico
            add_to_history(project_name, project_path, project_type)

            # Cria planilha se solicitado
            if self.create_spreadsheet_var.get():
                self.create_initial_spreadsheet(project_path, project_name, project_type)

            # Salva os serviços selecionados
            self.save_project_services(project_path)

            messagebox.showinfo(
                "Sucesso",
                f"Projeto '{project_name}' criado com sucesso em:\n{project_path}"
            )

            # Atualiza o diretório padrão nas configurações
            self.config['default_dir'] = base_dir

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar projeto:\n{str(e)}")

    def get_selected_services(self):
        """Retorna os serviços selecionados pelo usuário"""
        return {
            service_type: var.get()
            for service_type, var in self.selected_services.items()
            if var.get()
        }

    def save_project_services(self, project_path):
        """Salva os serviços selecionados em um arquivo no projeto"""
        services_file = os.path.join(project_path, 'project_services.json')
        with open(services_file, 'w') as f:
            json.dump(self.get_selected_services(), f, indent=4)

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