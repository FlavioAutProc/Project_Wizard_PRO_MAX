import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from ui.main_window import MainWindow
from core.utils import setup_data_files


class ProjectWizardApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Wizard PRO MAX")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        # Configuração inicial
        setup_data_files()

        # Carrega configurações
        self.config = self.load_config()

        # Aplica tema
        self.apply_theme(self.config.get('theme', 'light'))

        # Cria a interface principal
        self.main_window = MainWindow(self.root, self.config)

        # Configura o fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_config(self):
        """Carrega as configurações do arquivo config.json"""
        try:
            with open('data/config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Configuração padrão
            return {
                'theme': 'light',
                'default_dir': os.path.expanduser('~/Documents/Projects'),
                'recent_projects': [],
                'pomodoro_duration': 25
            }

    def save_config(self):
        """Salva as configurações no arquivo config.json"""
        with open('data/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def apply_theme(self, theme):
        """Aplica o tema selecionado"""
        if theme == 'dark':
            self.root.tk_setPalette(
                background='#2d2d2d',
                foreground='#ffffff',
                activeBackground='#3d3d3d',
                activeForeground='#ffffff'
            )
        else:
            self.root.tk_setPalette(
                background='#f0f0f0',
                foreground='#000000',
                activeBackground='#e0e0e0',
                activeForeground='#000000'
            )

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