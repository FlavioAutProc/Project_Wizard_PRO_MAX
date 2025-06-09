import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser
import os

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

    def __init__(self, parent_frame):
        self.parent = parent_frame
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

    def setup_apps_tab(self):
        """Configura a aba de aplicativos com estilo moderno"""
        self.apps_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.apps_tab, text="🖥️ Aplicativos")

        for i, (app_name, _) in enumerate(self.APPS.items()):
            btn = ttk.Button(
                self.apps_tab,
                text=f"▶ Abrir {app_name}",
                command=lambda name=app_name: self.open_app(name),
                bootstyle="outline" if HAS_TTKBOOTSTRAP else None,
                width=20
            )
            btn.grid(row=i, column=0, padx=10, pady=8, sticky=tk.EW)

        self.apps_tab.columnconfigure(0, weight=1)

    def setup_links_tab(self):
        """Configura a aba de links rápidos com estilo moderno"""
        self.links_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.links_tab, text="🌐 Links Rápidos")

        for i, (link_name, _) in enumerate(self.QUICK_LINKS.items()):
            btn = ttk.Button(
                self.links_tab,
                text=f"🌐 {link_name}",
                command=lambda name=link_name: self.open_link(name),
                bootstyle="outline" if HAS_TTKBOOTSTRAP else None,
                width=20
            )
            btn.grid(row=i, column=0, padx=10, pady=8, sticky=tk.EW)

        self.links_tab.columnconfigure(0, weight=1)

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