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
        self.root.title("Project Wizard PRO MAX 3.0")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        setup_data_files()
        self.config = self.load_config()
        self.setup_theme_and_styles()

        self.main_window = MainWindow(self.root, self.config)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_config(self):
        """Carrega configurações com valores padrão"""
        default_config = {
            'theme': 'dark',
            'default_dir': os.path.expanduser('~/Documents/Projects'),
            'recent_projects': [],
            'pomodoro_duration': 25,
            'font_size': 10,
            'font_family': 'Segoe UI' if os.name == 'nt' else 'Helvetica'
        }

        try:
            with open('data/config.json', 'r') as f:
                return {**default_config, **json.load(f)}
        except (FileNotFoundError, json.JSONDecodeError):
            return default_config

    def setup_theme_and_styles(self):
        """Configura tema e estilos visuais"""
        if HAS_TTKBOOTSTRAP:
            theme = 'darkly' if self.config.get('theme', 'dark') == 'dark' else 'minty'
            self.style = Style(theme=theme)
            self.root.style = self.style
        else:
            self.apply_basic_theme(self.config.get('theme', 'dark'))

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(
            family=self.config.get('font_family'),
            size=self.config.get('font_size', 10)
        )

    def save_config(self):
        """Salva configurações no arquivo"""
        with open('data/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def on_close(self):
        """Ação ao fechar a aplicação"""
        self.save_config()
        self.root.destroy()

    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ProjectWizardApp()
    app.run()