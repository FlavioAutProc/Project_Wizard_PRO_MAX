import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime

class ExcelGenerator:
    SPREADSHEET_TYPES = {
        "Controle de Estoque": ["Item", "Quantidade", "Localização", "Fornecedor", "Última Atualização"],
        "Planejamento Financeiro": ["Categoria", "Orçamento", "Gasto", "Saldo", "Período"],
        "Controle de Tarefas": ["Tarefa", "Responsável", "Prazo", "Status", "Prioridade"],
        "Registro de Estudos": ["Tópico", "Data", "Horas", "Status", "Notas"],
        "Controle de Produção": ["Produto", "Quantidade", "Data Início", "Data Fim", "Status"],
        "Personalizado": []
    }
    
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        self.frame = ttk.LabelFrame(self.parent, text="Gerar Planilha Personalizada", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tipo de Planilha
        ttk.Label(self.frame, text="Tipo de Planilha:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.spreadsheet_type_combo = ttk.Combobox(
            self.frame, 
            values=list(self.SPREADSHEET_TYPES.keys()), 
            width=30
        )
        self.spreadsheet_type_combo.grid(row=0, column=1, sticky=tk.EW, pady=(0, 5), padx=(5, 0))
        self.spreadsheet_type_combo.current(0)
        self.spreadsheet_type_combo.bind("<<ComboboxSelected>>", self.update_headers)
        
        # Nome da Planilha
        ttk.Label(self.frame, text="Nome da Planilha:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.spreadsheet_name_entry = ttk.Entry(self.frame, width=30)
        self.spreadsheet_name_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 5), padx=(5, 0))
        self.spreadsheet_name_entry.insert(0, "controle_")
        
        # Número de Linhas Iniciais
        ttk.Label(self.frame, text="Linhas Iniciais:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.initial_rows_spin = ttk.Spinbox(self.frame, from_=0, to=1000, width=10)
        self.initial_rows_spin.grid(row=2, column=1, sticky=tk.W, pady=(0, 5), padx=(5, 0))
        self.initial_rows_spin.set(10)
        
        # Cabeçalhos
        ttk.Label(self.frame, text="Cabeçalhos:").grid(row=3, column=0, sticky=tk.NW, pady=(0, 5))
        self.headers_frame = ttk.Frame(self.frame)
        self.headers_frame.grid(row=3, column=1, sticky=tk.NSEW, pady=(0, 5))
        
        self.headers_text = tk.Text(self.headers_frame, width=30, height=5)
        self.headers_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.headers_frame, command=self.headers_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.headers_text.config(yscrollcommand=scrollbar.set)
        
        # Atualiza os cabeçalhos iniciais
        self.update_headers()
        
        # Diretório de Saída
        ttk.Label(self.frame, text="Salvar em:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.dir_frame = ttk.Frame(self.frame)
        self.dir_frame.grid(row=4, column=1, sticky=tk.EW, pady=(0, 5))
        
        self.dir_entry = ttk.Entry(self.dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.dir_entry.insert(0, os.path.expanduser("~/Documents"))
        
        self.browse_btn = ttk.Button(self.dir_frame, text="...", width=3, command=self.browse_directory)
        self.browse_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Botão de Geração
        self.generate_btn = ttk.Button(self.frame, text="Gerar Planilha", command=self.generate_spreadsheet)
        self.generate_btn.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky=tk.EW)
        
        # Configura o redimensionamento
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(3, weight=1)
    
    def update_headers(self, event=None):
        """Atualiza os cabeçalhos com base no tipo selecionado"""
        selected_type = self.spreadsheet_type_combo.get()
        headers = self.SPREADSHEET_TYPES.get(selected_type, [])
        
        self.headers_text.delete(1.0, tk.END)
        self.headers_text.insert(tk.END, "\n".join(headers))
        
        # Atualiza o nome da planilha se não foi modificado pelo usuário
        current_name = self.spreadsheet_name_entry.get()
        if current_name == "controle_" or not current_name:
            self.spreadsheet_name_entry.delete(0, tk.END)
            self.spreadsheet_name_entry.insert(0, f"controle_{selected_type.lower().replace(' ', '_')}")
    
    def browse_directory(self):
        """Abre um diálogo para selecionar o diretório de saída"""
        from tkinter import filedialog
        dir_path = filedialog.askdirectory(
            initialdir=self.dir_entry.get(),
            title="Selecione o diretório para salvar a planilha"
        )
        if dir_path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir_path)
    
    def generate_spreadsheet(self):
        """Gera a planilha Excel com as configurações definidas"""
        try:
            # Obtém os parâmetros
            spreadsheet_name = self.spreadsheet_name_entry.get().strip()
            if not spreadsheet_name.endswith('.xlsx'):
                spreadsheet_name += '.xlsx'
            
            output_dir = self.dir_entry.get().strip()
            if not output_dir:
                raise ValueError("Selecione um diretório para salvar a planilha")
            
            # Obtém os cabeçalhos
            headers_text = self.headers_text.get(1.0, tk.END).strip()
            headers = [h.strip() for h in headers_text.split('\n') if h.strip()]
            
            if not headers:
                raise ValueError("Insira pelo menos um cabeçalho para a planilha")
            
            # Cria o DataFrame
            num_rows = int(self.initial_rows_spin.get())
            data = {header: [""] * num_rows for header in headers}
            df = pd.DataFrame(data)
            
            # Cria o caminho completo e salva
            output_path = os.path.join(output_dir, spreadsheet_name)
            
            # Verifica se o arquivo já existe
            if os.path.exists(output_path):
                response = messagebox.askyesno(
                    "Arquivo Existente",
                    f"O arquivo '{spreadsheet_name}' já existe. Deseja substituir?"
                )
                if not response:
                    return
            
            df.to_excel(output_path, index=False)
            messagebox.showinfo(
                "Sucesso", 
                f"Planilha '{spreadsheet_name}' gerada com sucesso em:\n{output_dir}"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar planilha:\n{str(e)}")