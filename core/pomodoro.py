import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from datetime import datetime, timedelta

class PomodoroTimer:
    def __init__(self, parent_frame, config):
        self.parent = parent_frame
        self.config = config
        self.running = False
        self.remaining = self.config.get('pomodoro_duration', 25) * 60
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        self.frame = ttk.LabelFrame(self.parent, text="Pomodoro Timer", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display do tempo
        self.time_label = ttk.Label(
            self.frame, 
            text=self.format_time(self.remaining), 
            font=('Helvetica', 24)
        )
        self.time_label.pack(pady=(0, 10))
        
        # Controles
        self.controls_frame = ttk.Frame(self.frame)
        self.controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_btn = ttk.Button(
            self.controls_frame, 
            text="Iniciar", 
            command=self.start_timer
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(
            self.controls_frame, 
            text="Pausar", 
            command=self.pause_timer,
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(
            self.controls_frame, 
            text="Resetar", 
            command=self.reset_timer
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Configuração da duração
        self.settings_frame = ttk.Frame(self.frame)
        self.settings_frame.pack(fill=tk.X)
        
        ttk.Label(self.settings_frame, text="Duração (min):").pack(side=tk.LEFT)
        
        self.duration_spin = ttk.Spinbox(
            self.settings_frame, 
            from_=1, 
            to=120, 
            width=5,
            command=self.update_duration
        )
        self.duration_spin.pack(side=tk.LEFT, padx=5)
        self.duration_spin.set(self.config.get('pomodoro_duration', 25))
        
        # Tempo estimado de término
        self.end_time_label = ttk.Label(
            self.frame, 
            text="",
            font=('Helvetica', 10)
        )
        self.update_end_time_label()
        self.end_time_label.pack()
    
    def format_time(self, seconds):
        """Formata o tempo em MM:SS"""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"
    
    def update_duration(self):
        """Atualiza a duração do Pomodoro"""
        try:
            duration = int(self.duration_spin.get())
            self.config['pomodoro_duration'] = duration
            self.remaining = duration * 60
            self.time_label.config(text=self.format_time(self.remaining))
            self.update_end_time_label()
        except ValueError:
            pass
    
    def update_end_time_label(self):
        """Atualiza o rótulo com o tempo estimado de término"""
        now = datetime.now()
        end_time = now + timedelta(seconds=self.remaining)
        self.end_time_label.config(
            text=f"Término estimado: {end_time.strftime('%H:%M')}"
        )
    
    def start_timer(self):
        """Inicia o timer"""
        if not self.running:
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.thread = threading.Thread(target=self.run_timer, daemon=True)
            self.thread.start()
            self.update_end_time_label()
    
    def pause_timer(self):
        """Pausa o timer"""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
    
    def reset_timer(self):
        """Reseta o timer para a duração configurada"""
        self.running = False
        self.remaining = self.config.get('pomodoro_duration', 25) * 60
        self.time_label.config(text=self.format_time(self.remaining))
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.update_end_time_label()
    
    def run_timer(self):
        """Executa o timer em uma thread separada"""
        while self.remaining > 0 and self.running:
            time.sleep(1)
            self.remaining -= 1
            self.time_label.config(text=self.format_time(self.remaining))
            self.parent.update()
        
        if self.remaining == 0 and self.running:
            self.running = False
            self.show_completion_alert()
    
    def show_completion_alert(self):
        """Mostra um alerta quando o timer é concluído"""
        messagebox.showinfo(
            "Pomodoro Completo", 
            "O tempo do Pomodoro terminou! Hora de fazer uma pausa."
        )
        self.reset_timer()