import tkinter as tk
from tkinter import ttk, font, messagebox
import os
import json
from ui.main_window import MainWindow
from core.utils import setup_data_files

try:
    from ttkbootstrap import Style

    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False


class ProjectWizardApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Wizard PRO MAX")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        # Configuração inicial
        setup_data_files()

        # Carrega configurações
        self.config = self.load_config()

        # Configura tema e estilo
        self.setup_theme_and_styles()

        # Cria a interface principal
        self.main_window = MainWindow(self.root, self.config)

        # Configura o fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_config(self):
        """Carrega as configurações do arquivo config.json"""
        try:
            with open('data/config.json', 'r') as f:
                config = json.load(f)
                # Garante que todas as chaves necessárias existam
                default_config = {
                    'theme': 'dark',
                    'default_dir': os.path.expanduser('~/Documents/Projects'),
                    'recent_projects': [],
                    'pomodoro_duration': 25,
                    'font_size': 10,
                    'font_family': 'Segoe UI' if os.name == 'nt' else 'Helvetica'
                }
                return {**default_config, **config}
        except (FileNotFoundError, json.JSONDecodeError):
            return default_config

    def setup_theme_and_styles(self):
        """Configura o tema e estilos da aplicação"""
        if HAS_TTKBOOTSTRAP:
            self.style = Style(theme='darkly')
            self.root.style = self.style
        else:
            self.apply_basic_theme(self.config.get('theme', 'dark'))

        # Configura fonte padrão
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(
            family=self.config.get('font_family', 'Segoe UI' if os.name == 'nt' else 'Helvetica'),
            size=self.config.get('font_size', 10)
        )

    def apply_basic_theme(self, theme_name):
        """Aplica um tema básico quando ttkbootstrap não está disponível"""
        theme = {
            'dark': {
                'bg': '#2d2d2d',
                'fg': '#e6e6e6',
                'active_bg': '#3d3d3d',
                'active_fg': '#ffffff',
                'select_bg': '#4d4d4d',
                'select_fg': '#ffffff'
            },
            'light': {
                'bg': '#f5f5f5',
                'fg': '#333333',
                'active_bg': '#e0e0e0',
                'active_fg': '#000000',
                'select_bg': '#d0d0d0',
                'select_fg': '#000000'
            }
        }.get(theme_name, 'dark')

        self.root.tk_setPalette(
            background=theme['bg'],
            foreground=theme['fg'],
            activeBackground=theme['active_bg'],
            activeForeground=theme['active_fg'],
            selectColor=theme['select_bg'],
            selectBackground=theme['select_bg'],
            selectForeground=theme['select_fg']
        )

        style = ttk.Style()
        style.configure('.', font=('TkDefaultFont'))
        style.configure('TFrame', background=theme['bg'])
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('TButton', background=theme['active_bg'], foreground=theme['active_fg'])
        style.configure('TEntry', fieldbackground=theme['bg'], foreground=theme['fg'])
        style.configure('TCombobox', fieldbackground=theme['bg'], foreground=theme['fg'])
        style.configure('TNotebook', background=theme['bg'])
        style.configure('TNotebook.Tab', background=theme['bg'], foreground=theme['fg'])

    def save_config(self):
        """Salva as configurações no arquivo config.json"""
        with open('data/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def on_close(self):
        """Lida com o fechamento da aplicação"""
        self.save_config()
        self.root.destroy()

    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ProjectWizardApp()
    app.run()