import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser
import os
import json

from future.moves.tkinter import filedialog

from core.utils import clean_temp_files

try:
    from ttkbootstrap import Style

    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False


class AutomationTools:
    APPS = {
        "VS Code": "code",
        "Excel": "excel",
        "Navegador": "start chrome",
        "Terminal": "cmd" if os.name == 'nt' else "gnome-terminal",
        "Explorador de Arquivos": "explorer" if os.name == 'nt' else "nautilus"
    }

    QUICK_LINKS = {
        "ChatGPT": "https://chat.openai.com",
        "Google Drive": "https://drive.google.com",
        "Gmail": "https://mail.google.com",
        "GitHub": "https://github.com",
        "Instagram": "https://instagram.com"
    }

    SERVICE_AUTOMATIONS = {
        "MySQL": {
            "Iniciar Servidor": "sudo service mysql start",
            "Parar Servidor": "sudo service mysql stop",
            "Abrir CLI": "mysql -u root -p"
        },
        "PostgreSQL": {
            "Iniciar Servidor": "sudo service postgresql start",
            "Parar Servidor": "sudo service postgresql stop",
            "Abrir CLI": "psql -U postgres"
        },
        "React": {
            "Iniciar Dev Server": "npm start",
            "Build para Produção": "npm run build",
            "Instalar Dependências": "npm install"
        },
        "Node.js": {
            "Iniciar Servidor": "node server.js",
            "Instalar Dependências": "npm install",
            "Rodar Tests": "npm test"
        }
    }

    def __init__(self, parent_frame, config):
        self.parent = parent_frame
        self.config = config
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do usuário com estilo moderno"""
        self.frame = ttk.LabelFrame(
            self.parent,
            text="Utilitários e Automação",
            padding=(15, 10),
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Abas
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Configuração das abas
        self.setup_apps_tab()
        self.setup_links_tab()
        self.setup_commands_tab()
        self.setup_cleanup_tab()
        self.setup_service_automations_tab()

    def setup_apps_tab(self):
        """Configura a aba de aplicativos com estilo moderno"""
        self.apps_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.apps_tab, text="🖥️ Aplicativos")

        # Organiza em cards
        for i, (app_name, _) in enumerate(self.APPS.items()):
            card = ttk.Frame(
                self.apps_tab,
                padding=10,
                relief="ridge",
                borderwidth=2
            )
            card.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky=tk.NSEW)

            ttk.Label(card, text=app_name).pack(pady=(0, 5))

            btn = ttk.Button(
                card,
                text="▶ Abrir",
                command=lambda name=app_name: self.open_app(name),
                bootstyle="outline" if HAS_TTKBOOTSTRAP else None,
                width=15
            )
            btn.pack()

        # Configura o redimensionamento
        for i in range(2):
            self.apps_tab.columnconfigure(i, weight=1)

    def setup_links_tab(self):
        """Configura a aba de links rápidos com estilo moderno"""
        self.links_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.links_tab, text="🌐 Links Rápidos")

        # Organiza em cards
        for i, (link_name, _) in enumerate(self.QUICK_LINKS.items()):
            card = ttk.Frame(
                self.links_tab,
                padding=10,
                relief="ridge",
                borderwidth=2
            )
            card.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky=tk.NSEW)

            ttk.Label(card, text=link_name).pack(pady=(0, 5))

            btn = ttk.Button(
                card,
                text="🌐 Abrir",
                command=lambda name=link_name: self.open_link(name),
                bootstyle="outline" if HAS_TTKBOOTSTRAP else None,
                width=15
            )
            btn.pack()

        # Configura o redimensionamento
        for i in range(3):
            self.links_tab.columnconfigure(i, weight=1)

    def setup_commands_tab(self):
        """Configura a aba de comandos personalizados com estilo moderno"""
        self.commands_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.commands_tab, text="⌨️ Comandos")

        # Campo para comando personalizado
        ttk.Label(self.commands_tab, text="Comando:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))

        self.command_entry = ttk.Entry(self.commands_tab)
        self.command_entry.grid(
            row=0, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))

        # Botão de execução
        self.run_btn = ttk.Button(
            self.commands_tab,
            text="⚡ Executar Comando",
            command=self.run_custom_command,
            bootstyle="success" if HAS_TTKBOOTSTRAP else None
        )
        self.run_btn.grid(
            row=1, column=0, columnspan=2, pady=(10, 0), sticky=tk.EW)

        # Configura redimensionamento
        self.commands_tab.columnconfigure(1, weight=1)

    def setup_cleanup_tab(self):
        """Configura a aba de limpeza de arquivos temporários"""
        self.cleanup_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.cleanup_tab, text="🧹 Limpeza")

        # Card para limpeza de arquivos temporários
        card = ttk.LabelFrame(
            self.cleanup_tab,
            text="Limpeza de Arquivos Temporários",
            padding=10,
            bootstyle="warning" if HAS_TTKBOOTSTRAP else None
        )
        card.pack(fill=tk.X, pady=5)

        ttk.Label(card, text="Diretório para limpar:").pack(anchor=tk.W)

        self.cleanup_dir_entry = ttk.Entry(card)
        self.cleanup_dir_entry.pack(fill=tk.X, pady=(0, 10))
        self.cleanup_dir_entry.insert(0, os.path.expanduser("~"))

        ttk.Button(
            card,
            text="📂 Selecionar Diretório",
            command=self.browse_cleanup_dir,
            bootstyle="outline" if HAS_TTKBOOTSTRAP else None
        ).pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            card,
            text="🧹 Limpar Arquivos Temporários",
            command=self.clean_temp_files,
            bootstyle="danger" if HAS_TTKBOOTSTRAP else None
        ).pack(fill=tk.X)

        # Área para mostrar resultados
        self.cleanup_result = ttk.Label(
            self.cleanup_tab,
            text="",
            wraplength=400
        )
        self.cleanup_result.pack(fill=tk.X, pady=10)

    def setup_service_automations_tab(self):
        """Configura a aba de automações por serviço"""
        self.service_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.service_tab, text="⚙️ Automações")

        # Combo para selecionar o tipo de serviço
        ttk.Label(self.service_tab, text="Serviço:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))

        self.service_combo = ttk.Combobox(
            self.service_tab,
            values=list(self.SERVICE_AUTOMATIONS.keys()),
            state="readonly",
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.service_combo.grid(
            row=0, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))
        self.service_combo.bind("<<ComboboxSelected>>", self.update_service_commands)

        # Frame para os comandos do serviço
        self.service_commands_frame = ttk.Frame(self.service_tab)
        self.service_commands_frame.grid(
            row=1, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 10))

        # Configura o redimensionamento
        self.service_tab.columnconfigure(1, weight=1)
        self.service_tab.rowconfigure(1, weight=1)

    def update_service_commands(self, event=None):
        """Atualiza os comandos disponíveis para o serviço selecionado"""
        # Limpa os comandos anteriores
        for widget in self.service_commands_frame.winfo_children():
            widget.destroy()

        # Obtém o serviço selecionado
        service = self.service_combo.get()
        if not service:
            return

        # Cria cards para cada comando
        commands = self.SERVICE_AUTOMATIONS.get(service, {})
        for i, (cmd_name, cmd) in enumerate(commands.items()):
            card = ttk.Frame(
                self.service_commands_frame,
                padding=10,
                relief="ridge",
                borderwidth=2
            )
            card.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky=tk.NSEW)

            ttk.Label(card, text=cmd_name).pack(pady=(0, 5))

            btn = ttk.Button(
                card,
                text="▶ Executar",
                command=lambda c=cmd: self.run_service_command(c),
                bootstyle="outline" if HAS_TTKBOOTSTRAP else None,
                width=15
            )
            btn.pack()

        # Configura o redimensionamento
        for i in range(2):
            self.service_commands_frame.columnconfigure(i, weight=1)

    def browse_cleanup_dir(self):
        """Abre o diálogo para selecionar diretório de limpeza"""
        dir_path = filedialog.askdirectory(
            initialdir=self.cleanup_dir_entry.get(),
            title="Selecione o diretório para limpar"
        )
        if dir_path:
            self.cleanup_dir_entry.delete(0, tk.END)
            self.cleanup_dir_entry.insert(0, dir_path)

    def clean_temp_files(self):
        """Executa a limpeza de arquivos temporários"""
        dir_path = self.cleanup_dir_entry.get().strip()
        if not dir_path:
            messagebox.showwarning("Aviso", "Selecione um diretório para limpar")
            return

        try:
            removed_files = clean_temp_files(dir_path)
            if removed_files:
                self.cleanup_result.config(
                    text=f"Removidos {len(removed_files)} arquivos temporários.\n"
                         f"Primeiros arquivos: {', '.join(os.path.basename(f) for f in removed_files[:3])}"
                )
            else:
                self.cleanup_result.config(text="Nenhum arquivo temporário encontrado para remover.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao limpar arquivos temporários:\n{str(e)}")

    def open_app(self, app_name):
        """Abre o aplicativo especificado"""
        try:
            command = self.APPS[app_name]
            if os.name == 'nt':  # Windows
                if command.startswith('start '):
                    subprocess.Popen(command, shell=True)
                else:
                    os.startfile(command)
            else:  # Linux/Mac
                subprocess.Popen(command.split())
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir {app_name}:\n{str(e)}")

    def open_link(self, link_name):
        """Abre o link especificado no navegador padrão"""
        try:
            url = self.QUICK_LINKS[link_name]
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir {link_name}:\n{str(e)}")

    def run_custom_command(self):
        """Executa um comando personalizado"""
        command = self.command_entry.get().strip()
        if not command:
            messagebox.showwarning("Aviso", "Insira um comando para executar")
            return

        try:
            subprocess.Popen(command, shell=True)
            messagebox.showinfo("Sucesso", f"Comando executado: {command}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao executar comando:\n{str(e)}")

    def run_service_command(self, command):
        """Executa um comando de serviço específico"""
        try:
            subprocess.Popen(command, shell=True)
            messagebox.showinfo("Sucesso", f"Comando de serviço executado: {command}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao executar comando de serviço:\n{str(e)}")