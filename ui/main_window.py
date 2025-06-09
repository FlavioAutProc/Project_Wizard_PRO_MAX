import tkinter as tk
from tkinter import ttk
from ui.tabs import ProjectTab, SpreadsheetTab, UtilitiesTab, HistoryTab, SettingsTab

class MainWindow:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface principal"""
        # Barra de menu
        self.setup_menu()
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Cria as abas
        self.tabs = {
            "project": ProjectTab(self.notebook, self.config),
            "spreadsheet": SpreadsheetTab(self.notebook),
            "utilities": UtilitiesTab(self.notebook, self.config),
            "history": HistoryTab(self.notebook),
            "settings": SettingsTab(self.notebook, self.config)
        }
        
        # Adiciona as abas ao notebook
        self.notebook.add(self.tabs["project"].frame, text="Novo Projeto")
        self.notebook.add(self.tabs["spreadsheet"].frame, text="Planilhas")
        self.notebook.add(self.tabs["utilities"].frame, text="Utilitários")
        self.notebook.add(self.tabs["history"].frame, text="Histórico")
        self.notebook.add(self.tabs["settings"].frame, text="Configurações")
    
    def setup_menu(self):
        """Configura a barra de menu"""
        menubar = tk.Menu(self.root)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self.show_about)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def show_about(self):
        """Mostra a janela 'Sobre'"""
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre o Project Wizard PRO MAX")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        ttk.Label(
            about_window, 
            text="Project Wizard PRO MAX\n\nVersão 1.0\n\nSistema de produtividade pessoal\npara automação de tarefas e gerenciamento de projetos",
            justify=tk.CENTER,
            font=('Helvetica', 12)
        ).pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Button(
            about_window, 
            text="Fechar", 
            command=about_window.destroy
        ).pack(pady=(0, 20))