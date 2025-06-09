import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from datetime import datetime, timedelta

try:
    from ttkbootstrap import Style, Meter

    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False


class PomodoroTimer:
    def __init__(self, parent_frame, config):
        self.parent = parent_frame
        self.config = config
        self.running = False
        self.remaining = self.config.get('pomodoro_duration', 25) * 60
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do usuário com estilo moderno"""
        self.frame = ttk.LabelFrame(
            self.parent,
            text="Pomodoro Timer",
            padding=(15, 10),
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Display do tempo
        if HAS_TTKBOOTSTRAP:
            self.time_meter = Meter(
                self.frame,
                metersize=180,
                padding=20,
                amountused=100,
                metertype="full",
                subtext="Tempo Restante",
                bootstyle="info",
                interactive=False
            )
            self.time_meter.pack(pady=(0, 20))
            self.update_meter_display()
        else:
            self.time_label = ttk.Label(
                self.frame,
                text=self.format_time(self.remaining),
                font=('Helvetica', 24)
            )
            self.time_label.pack(pady=(0, 20))

        # Controles
        self.controls_frame = ttk.Frame(self.frame)
        self.controls_frame.pack(fill=tk.X, pady=(0, 20))

        self.start_btn = ttk.Button(
            self.controls_frame,
            text="▶ Iniciar",
            command=self.start_timer,
            bootstyle="success" if HAS_TTKBOOTSTRAP else None
        )
        self.start_btn.pack(side=tk.LEFT, padx=5, expand=True)

        self.pause_btn = ttk.Button(
            self.controls_frame,
            text="⏸ Pausar",
            command=self.pause_timer,
            state=tk.DISABLED,
            bootstyle="warning" if HAS_TTKBOOTSTRAP else None
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5, expand=True)

        self.reset_btn = ttk.Button(
            self.controls_frame,
            text="↻ Resetar",
            command=self.reset_timer,
            bootstyle="danger" if HAS_TTKBOOTSTRAP else None
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5, expand=True)

        # Configuração da duração
        self.settings_frame = ttk.Frame(self.frame)
        self.settings_frame.pack(fill=tk.X)

        ttk.Label(self.settings_frame, text="Duração (min):").pack(side=tk.LEFT)

        self.duration_spin = ttk.Spinbox(
            self.settings_frame,
            from_=1,
            to=120,
            width=5,
            command=self.update_duration,
            bootstyle="info" if HAS_TTKBOOTSTRAP else None
        )
        self.duration_spin.pack(side=tk.LEFT, padx=10)
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

    def update_meter_display(self):
        """Atualiza o display do medidor ou label"""
        if HAS_TTKBOOTSTRAP:
            percent = (self.remaining / (self.config.get('pomodoro_duration', 25) * 60)) * 100
            self.time_meter.configure(amountused=percent)
            # Atualiza o texto através do subtext
            self.time_meter.configure(subtext=self.format_time(self.remaining))
        else:
            self.time_label.config(text=self.format_time(self.remaining))

    def update_duration(self):
        """Atualiza a duração do Pomodoro"""
        try:
            duration = int(self.duration_spin.get())
            if duration < 1 or duration > 120:
                raise ValueError("Duração deve estar entre 1 e 120 minutos")

            self.config['pomodoro_duration'] = duration
            self.remaining = duration * 60

            if HAS_TTKBOOTSTRAP:
                self.time_meter.configure(amounttotal=duration * 60)

            self.update_meter_display()
            self.update_end_time_label()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            self.duration_spin.set(self.config.get('pomodoro_duration', 25))

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
        self.update_meter_display()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.update_end_time_label()

    def run_timer(self):
        """Executa o timer em uma thread separada"""
        while self.remaining > 0 and self.running:
            time.sleep(1)
            self.remaining -= 1
            self.update_meter_display()
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