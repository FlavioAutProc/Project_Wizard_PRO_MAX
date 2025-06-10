import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from docx import Document
from core.utils import add_note, get_notes, export_notes_to_docx
import json

try:
    from ttkbootstrap import Style

    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False


class NotesTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        """Configura a interface do usuário"""
        self.frame = ttk.Frame(self.parent)

        # Painel esquerdo - Lista de anotações
        self.list_frame = ttk.Frame(self.frame)
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Barra de ferramentas
        toolbar = ttk.Frame(self.list_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        self.search_entry = ttk.Entry(toolbar)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.search_notes)

        ttk.Button(
            toolbar,
            text="🔍",
            width=3,
            command=self.search_notes,
            bootstyle="outline" if HAS_TTKBOOTSTRAP else None
        ).pack(side=tk.LEFT)

        # Lista de anotações
        self.notes_list = tk.Listbox(
            self.list_frame,
            width=30,
            height=20,
            bg="#3d3d3d" if not HAS_TTKBOOTSTRAP else None,
            fg="white" if not HAS_TTKBOOTSTRAP else None
        )
        self.notes_list.pack(fill=tk.BOTH, expand=True)
        self.notes_list.bind("<<ListboxSelect>>", self.show_note_details)

        # Painel direito - Detalhes da anotação
        self.detail_frame = ttk.Frame(self.frame)
        self.detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Campos do formulário
        ttk.Label(self.detail_frame, text="Título:").pack(anchor=tk.W)
        self.title_entry = ttk.Entry(self.detail_frame)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.detail_frame, text="Tipo:").pack(anchor=tk.W)
        self.type_combo = ttk.Combobox(
            self.detail_frame,
            values=["geral", "trabalho", "pessoal", "estudo", "projeto"],
            state="readonly",
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.type_combo.pack(fill=tk.X, pady=(0, 10))
        self.type_combo.current(0)

        ttk.Label(self.detail_frame, text="Tags (separadas por vírgula):").pack(anchor=tk.W)
        self.tags_entry = ttk.Entry(self.detail_frame)
        self.tags_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.detail_frame, text="Conteúdo:").pack(anchor=tk.W)
        self.content_text = tk.Text(
            self.detail_frame,
            height=10,
            wrap=tk.WORD,
            bg="#3d3d3d" if not HAS_TTKBOOTSTRAP else None,
            fg="white" if not HAS_TTKBOOTSTRAP else None,
            insertbackground="white"
        )
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Barra de rolagem para o conteúdo
        scrollbar = ttk.Scrollbar(self.content_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.content_text.yview)

        # Botões de ação
        btn_frame = ttk.Frame(self.detail_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="➕ Nova",
            command=self.new_note,
            bootstyle="success" if HAS_TTKBOOTSTRAP else None
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="💾 Salvar",
            command=self.save_note,
            bootstyle="primary" if HAS_TTKBOOTSTRAP else None
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="🗑️ Excluir",
            command=self.delete_note,
            bootstyle="danger" if HAS_TTKBOOTSTRAP else None
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="📄 Exportar",
            command=self.export_note,
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        ).pack(side=tk.LEFT)

        # Variável para armazenar a anotação atual
        self.current_note = None

    def load_notes(self, search_term=None):
        """Carrega as anotações na lista"""
        self.notes_list.delete(0, tk.END)
        notes = get_notes()

        if search_term:
            search_term = search_term.lower()
            notes = [
                note for note in notes
                if (search_term in note['title'].lower() or
                    search_term in note['content'].lower() or
                    any(search_term in tag.lower() for tag in note.get('tags', [])))
            ]

        for note in notes:
            self.notes_list.insert(tk.END, note['title'])

        if notes:
            self.notes_list.selection_set(0)
            self.show_note_details()

    def search_notes(self, event=None):
        """Filtra as anotações com base no termo de busca"""
        search_term = self.search_entry.get()
        self.load_notes(search_term)

    def show_note_details(self, event=None):
        """Mostra os detalhes da anotação selecionada"""
        selection = self.notes_list.curselection()
        if not selection:
            return

        notes = get_notes()
        selected_note = notes[selection[0]]
        self.current_note = selected_note

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, selected_note['title'])

        self.type_combo.set(selected_note.get('type', 'geral'))

        self.tags_entry.delete(0, tk.END)
        self.tags_entry.insert(0, ', '.join(selected_note.get('tags', [])))

        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(tk.END, selected_note['content'])

    def new_note(self):
        """Cria uma nova anotação em branco"""
        self.notes_list.selection_clear(0, tk.END)
        self.current_note = None

        self.title_entry.delete(0, tk.END)
        self.type_combo.current(0)
        self.tags_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)

        self.title_entry.focus()

    def save_note(self):
        """Salva a anotação atual"""
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        note_type = self.type_combo.get()
        tags = [tag.strip() for tag in self.tags_entry.get().split(',') if tag.strip()]

        if not title:
            messagebox.showwarning("Aviso", "O título da anotação é obrigatório")
            return

        if not content:
            messagebox.showwarning("Aviso", "O conteúdo da anotação é obrigatório")
            return

        if self.current_note:
            # Atualiza a anotação existente
            self.update_note(title, content, tags, note_type)
        else:
            # Cria uma nova anotação
            add_note(title, content, tags, note_type)

        self.load_notes()
        messagebox.showinfo("Sucesso", "Anotação salva com sucesso!")

    def update_note(self, title, content, tags, note_type):
        """Atualiza uma anotação existente"""
        try:
            with open('data/notes.json', 'r+', encoding='utf-8') as f:
                notes = json.load(f)

                for note in notes:
                    if note['id'] == self.current_note['id']:
                        note['title'] = title
                        note['content'] = content
                        note['tags'] = tags
                        note['type'] = note_type
                        note['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        break

                f.seek(0)
                json.dump(notes, f, indent=4, ensure_ascii=False)
                f.truncate()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar anotação:\n{str(e)}")

    def delete_note(self):
        """Exclui a anotação atual"""
        if not self.current_note:
            messagebox.showwarning("Aviso", "Nenhuma anotação selecionada para excluir")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta anotação?"):
            return

        try:
            with open('data/notes.json', 'r+', encoding='utf-8') as f:
                notes = json.load(f)
                notes = [note for note in notes if note['id'] != self.current_note['id']]

                f.seek(0)
                json.dump(notes, f, indent=4, ensure_ascii=False)
                f.truncate()

            self.load_notes()
            self.new_note()
            messagebox.showinfo("Sucesso", "Anotação excluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir anotação:\n{str(e)}")

    def export_note(self):
        """Exporta a anotação atual para DOCX"""
        if not self.current_note:
            messagebox.showwarning("Aviso", "Nenhuma anotação selecionada para exportar")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Documento Word", "*.docx"), ("Todos os arquivos", "*.*")],
            initialfile=f"{self.current_note['title']}.docx"
        )

        if not file_path:
            return

        try:
            export_notes_to_docx([self.current_note], file_path)
            messagebox.showinfo("Sucesso", f"Anotação exportada com sucesso para:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar anotação:\n{str(e)}")