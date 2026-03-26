import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import queue
import yt_dlp
import os
import shutil  # Necessário para verificar o FFmpeg

# -----------------------------
# Download worker (thread)
# -----------------------------
def baixar_recurso(url, qualidade, pasta_destino: Path, status_queue: queue.Queue, idx: int, modo: str):
    """
    Realiza o download com base no modo selecionado usando yt-dlp.
    """
    try:
        status_queue.put(("status", idx, "andamento", f"Baixando ({modo}): {url}"))

        # Configuração base
        ydl_opts = {
            "outtmpl": str(pasta_destino / "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }

        if modo == "Só Áudio (MP3)":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": str(qualidade),
                }],
            })
            
        elif modo == "Só Áudio (WAV)":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                }],
            })
            
        elif modo == "Só Áudio (FLAC)":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "flac",
                }],
            })

        elif modo == "Vídeo sem Áudio":
            # Baixa apenas o melhor vídeo disponível (sem áudio) e força MP4
            ydl_opts.update({
                "format": "bestvideo[ext=mp4]/bestvideo",
                "postprocessors": [{
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }],
            })
            
        elif modo == "Vídeo (WebM - Alta Qualidade)":
            ydl_opts.update({
                "format": "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]",
                "merge_output_format": "webm",
            })
            
        elif modo == "Vídeo (MKV)":
            ydl_opts.update({
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mkv",
            })

        else:  # Padrão: "Tudo (Vídeo + Áudio MP4)"
            ydl_opts.update({
                # Tenta baixar mp4 nativo, senão baixa o melhor e converte
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
                "merge_output_format": "mp4",  # Força a união em MP4
                "postprocessors": [{
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }],
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_queue.put(("status", idx, "ok", f"Concluído: {url}"))
    except Exception as e:
        status_queue.put(("status", idx, "erro", f"Erro: {url} ({e})"))


# -----------------------------
# App
# -----------------------------
class BaixadorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Baixador de Recursos")
        
        # Define o ícone da janela se o arquivo existir
        icon_path = Path(__file__).parent / "imgs" / "icon-app.png"
        if icon_path.exists():
            try:
                self.icon_img = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, self.icon_img)
            except Exception as e:
                print(f"Erro ao carregar ícone: {e}")

        self.root.geometry("920x680")
        self.root.minsize(860, 600)

        self.status_queue = queue.Queue()
        self.processando = False
        self.total = 0
        self.concluidos = 0

        # Seu caminho fixo
        self.pasta_destino = Path(r"C:\Users\mathe\OneDrive\Desktop\git\audios")
        # Garante que a pasta existe, senão cria
        try:
            self.pasta_destino.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Erro ao criar pasta: {e}")

        self.qualidade_var = tk.StringVar(value="192")
        self.modo_var = tk.StringVar(value="Tudo (Vídeo + Áudio MP4)")
        self.pasta_var = tk.StringVar(value=str(self.pasta_destino))

        self._configurar_estilo()
        self._montar_ui()
        self._verificar_fila()
        self._verificar_ffmpeg()

    def _verificar_ffmpeg(self):
        """Verifica de forma multiplataforma se o FFmpeg está instalado e no PATH."""
        if not shutil.which("ffmpeg"):
            messagebox.showwarning(
                "FFmpeg não encontrado",
                "O FFmpeg não foi detectado no sistema.\n\n"
                "Sem ele, as conversões para WAV, FLAC, MP3 ou a mesclagem de áudio e vídeo em alta qualidade poderão falhar.\n\n"
                "Certifique-se de instalá-lo e adicioná-lo às variáveis de ambiente (PATH)."
            )

    def _configurar_estilo(self):
        self.COL_BG = "#0b1220"
        self.COL_SURFACE = "#111a2e"
        self.COL_SURFACE_2 = "#0f172a"
        self.COL_BORDER = "#1f2a44"
        self.COL_TEXT = "#e5e7eb"
        self.COL_MUTED = "#9ca3af"
        self.COL_ACCENT = "#60a5fa"
        self.COL_OK = "#22c55e"
        self.COL_ERR = "#ef4444"
        self.COL_WARN = "#f59e0b"

        self.root.configure(bg=self.COL_BG)
        style = ttk.Style()
        try: style.theme_use("clam")
        except: pass

        style.configure(".", background=self.COL_BG, foreground=self.COL_TEXT, 
                        fieldbackground=self.COL_SURFACE_2, bordercolor=self.COL_BORDER,
                        troughcolor=self.COL_SURFACE_2)
        style.configure("Card.TFrame", background=self.COL_SURFACE, borderwidth=1, relief="solid")
        style.configure("Title.TLabel", background=self.COL_BG, foreground=self.COL_TEXT, font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background=self.COL_BG, foreground=self.COL_MUTED, font=("Segoe UI", 10))
        style.configure("H.TLabel", background=self.COL_SURFACE, foreground=self.COL_TEXT, font=("Segoe UI", 11, "bold"))
        style.configure("P.TLabel", background=self.COL_SURFACE, foreground=self.COL_MUTED, font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), padding=(14, 10), background=self.COL_ACCENT, foreground="#071426")
        style.map("Accent.TButton", background=[("active", "#93c5fd"), ("disabled", "#334155")])
        style.configure("Ghost.TButton", font=("Segoe UI", 10), padding=(12, 9), background=self.COL_SURFACE_2, foreground=self.COL_TEXT)
        style.configure("TProgressbar", thickness=18, background=self.COL_ACCENT)

    def _montar_ui(self):
        header = ttk.Frame(self.root, style="Card.TFrame", padding=16)
        header.pack(fill="x", padx=16, pady=(16, 10))

        ttk.Label(header, text="Baixador de Recursos", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Selecione o formato desejado e adicione os links abaixo.", style="Subtitle.TLabel").pack(anchor="w", pady=(6, 0))

        body = ttk.Frame(self.root, padding=0)
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body.columnconfigure(0, weight=3); body.columnconfigure(1, weight=2); body.rowconfigure(0, weight=1)

        left = ttk.Frame(body, style="Card.TFrame", padding=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ttk.Label(left, text="URLs", style="H.TLabel").pack(anchor="w")
        text_frame = ttk.Frame(left, style="Card.TFrame", padding=0); text_frame.pack(fill="both", expand=True, pady=10)
        self.urls_text = tk.Text(text_frame, height=10, wrap="word", bg=self.COL_SURFACE_2, fg=self.COL_TEXT,
                                 insertbackground=self.COL_TEXT, relief="flat", highlightthickness=1,
                                 highlightbackground=self.COL_BORDER, font=("Segoe UI", 11))
        self.urls_text.pack(side="left", fill="both", expand=True)

        btn_row = ttk.Frame(left, style="Card.TFrame", padding=(0, 12))
        btn_row.pack(fill="x")
        self.btn_baixar = ttk.Button(btn_row, text="Iniciar Download", style="Accent.TButton", command=self.iniciar_downloads)
        self.btn_baixar.pack(side="left")
        ttk.Button(btn_row, text="Limpar", style="Ghost.TButton", command=self.limpar_urls).pack(side="left", padx=10)
        ttk.Button(btn_row, text="Colar", style="Ghost.TButton", command=self.colar_urls).pack(side="left")

        right = ttk.Frame(body, style="Card.TFrame", padding=16)
        right.grid(row=0, column=1, sticky="nsew")

        ttk.Label(right, text="Opções", style="H.TLabel").pack(anchor="w")

        # MODO DE DOWNLOAD
        modo_box = ttk.Frame(right, style="Card.TFrame", padding=12); modo_box.pack(fill="x", pady=(10, 5))
        ttk.Label(modo_box, text="O que baixar?", style="P.TLabel").pack(anchor="w")
        
        opcoes_modo = [
            "Tudo (Vídeo + Áudio MP4)", 
            "Vídeo (WebM - Alta Qualidade)",
            "Vídeo (MKV)",
            "Só Áudio (MP3)", 
            "Só Áudio (WAV)",
            "Só Áudio (FLAC)",
            "Vídeo sem Áudio"
        ]
        self.modo_combo = ttk.Combobox(modo_box, textvariable=self.modo_var, state="readonly", values=opcoes_modo)
        self.modo_combo.pack(fill="x", pady=(6, 0))

        # PASTA
        pasta_box = ttk.Frame(right, style="Card.TFrame", padding=12); pasta_box.pack(fill="x", pady=5)
        ttk.Label(pasta_box, text="Pasta de destino", style="P.TLabel").pack(anchor="w")
        pasta_row = ttk.Frame(pasta_box, style="Card.TFrame", padding=0); pasta_row.pack(fill="x", pady=(6, 0))
        
        self.pasta_entry = tk.Entry(pasta_row, textvariable=self.pasta_var, bg=self.COL_SURFACE_2, fg=self.COL_TEXT, 
                                   insertbackground=self.COL_TEXT, relief="flat", highlightthickness=1, highlightbackground=self.COL_BORDER)
        self.pasta_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)
        
        ttk.Button(pasta_row, text="...", width=3, style="Ghost.TButton", command=self.selecionar_pasta).pack(side="right")
        
        btn_abrir = ttk.Button(pasta_box, text="📂 Abrir Pasta", style="Ghost.TButton", command=self.abrir_pasta_local)
        btn_abrir.pack(fill="x", pady=(8, 0))

        # QUALIDADE MP3
        qual_box = ttk.Frame(right, style="Card.TFrame", padding=12); qual_box.pack(fill="x", pady=5)
        ttk.Label(qual_box, text="Qualidade MP3 (se aplicável)", style="P.TLabel").pack(anchor="w")
        self.qual_combo = ttk.Combobox(qual_box, textvariable=self.qualidade_var, state="readonly", values=["128", "192", "320"])
        self.qual_combo.pack(fill="x", pady=(6, 0))

        # PROGRESSO
        prog_box = ttk.Frame(right, style="Card.TFrame", padding=12); prog_box.pack(fill="x", pady=5)
        self.prog_label = ttk.Label(prog_box, text="0/0 concluídos", style="P.TLabel"); self.prog_label.pack(anchor="w")
        self.progress = ttk.Progressbar(prog_box, mode="determinate", maximum=100); self.progress.pack(fill="x", pady=5)

        # LOG
        log_box = ttk.Frame(right, style="Card.TFrame", padding=12); log_box.pack(fill="both", expand=True)
        self.log_text = tk.Text(log_box, height=8, bg=self.COL_SURFACE_2, fg=self.COL_TEXT, relief="flat", font=("Consolas", 9), state="disabled")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.tag_configure("ok", foreground=self.COL_OK); self.log_text.tag_configure("erro", foreground=self.COL_ERR)
        self.log_text.tag_configure("andamento", foreground=self.COL_ACCENT)

    def log(self, msg: str, tag: str = None):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n", tag)
        self.log_text.configure(state="disabled"); self.log_text.see("end")

    def colar_urls(self):
        try: self.urls_text.insert("end", self.root.clipboard_get())
        except: pass

    def limpar_urls(self): self.urls_text.delete("1.0", "end")

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta: self.pasta_var.set(pasta)

    def abrir_pasta_local(self):
        """Abre a pasta de destino no Explorador de Arquivos"""
        path = self.pasta_var.get()
        if os.path.isdir(path):
            # Tenta usar os.startfile (Windows), se falhar (Linux/WSL), tenta usar xdg-open
            try:
                os.startfile(path)
            except AttributeError:
                import subprocess
                subprocess.call(['xdg-open', path])
        else:
            messagebox.showwarning("Aviso", "A pasta especificada não existe.")

    def iniciar_downloads(self):
        if self.processando: return
        urls = [u for u in self.urls_text.get("1.0", "end").splitlines() if u.strip().startswith("http")]
        if not urls:
            messagebox.showerror("Erro", "Insira URLs válidas.")
            return

        self.processando = True
        self.btn_baixar.configure(state="disabled")
        self.total = len(urls); self.concluidos = 0
        
        threading.Thread(target=self._thread_downloads, 
                         args=(urls, self.qualidade_var.get(), Path(self.pasta_var.get()), self.modo_var.get()), 
                         daemon=True).start()

    def _thread_downloads(self, urls, qualidade, pasta, modo):
        for i, url in enumerate(urls):
            baixar_recurso(url, qualidade, pasta, self.status_queue, i, modo)
            self.status_queue.put(("done_one", None, None, None))
        self.status_queue.put(("finished", None, None, None))

    def _verificar_fila(self):
        try:
            while True:
                item = self.status_queue.get_nowait()
                if item[0] == "status": self.log(item[3], item[2])
                elif item[0] == "done_one":
                    self.concluidos += 1
                    self.progress["value"] = (self.concluidos / self.total) * 100
                    self.prog_label.configure(text=f"{self.concluidos}/{self.total} concluídos")
                elif item[0] == "finished":
                    self.processando = False
                    self.btn_baixar.configure(state="normal")
                    self.log("Downloads finalizados.", "ok")
        except queue.Empty: pass
        self.root.after(150, self._verificar_fila)

if __name__ == "__main__":
    root = tk.Tk()
    app = BaixadorApp(root)
    root.mainloop()