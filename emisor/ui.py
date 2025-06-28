import tkinter as tk
from PIL import Image, ImageTk
import cv2

class EmitterUI:
    def __init__(self, emitter):
        self.emitter = emitter
        self.root = tk.Tk()
        self.root.title("TikTokLive - Emisor")
        self.root.geometry("900x700")
        self.streaming = False

        # Frame del menú principal
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(expand=True)

        self.title_label = tk.Label(self.menu_frame, text="TikTokLive", font=("Arial", 32, "bold"))
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(self.menu_frame, text="Iniciar transmisión", font=("Arial", 18), command=self.start_stream)
        self.start_button.pack(pady=20)

        self.quit_button = tk.Button(self.menu_frame, text="Salir", font=("Arial", 14), command=self.root.quit)
        self.quit_button.pack(pady=20)

        # Frame para la transmisión
        self.stream_frame = tk.Frame(self.root)
        self.video_label = tk.Label(self.stream_frame, width=800, height=500, bg="black")
        self.video_label.pack(pady=20)

        # Menú de filtros (visible durante la transmisión)
        self.filters = [
            "Ninguno", "Grises", "Sepia", "Invertir", "Espejo vertical", "Espejo horizontal",
            "Desenfoque", "Nitidez", "Bordes", "Detección de rostros", "Bigote", "Barba", "Lentes", "Sombrero", "Maquillaje"
        ]
        self.selected_filter = tk.StringVar(value=self.filters[0])
        self.filter_menu = tk.OptionMenu(self.stream_frame, self.selected_filter, *self.filters, command=self.change_filter)
        self.filter_menu.config(font=("Arial", 14))
        self.filter_menu.pack(pady=10)

        self.stop_button = tk.Button(self.stream_frame, text="Terminar transmisión", font=("Arial", 14), command=self.stop_stream)
        self.stop_button.pack(pady=20)

    def start(self):
        self.root.mainloop()

    def start_stream(self):
        self.menu_frame.pack_forget()
        self.stream_frame.pack(expand=True)
        self.streaming = True
        self.emitter.current_filter = self.selected_filter.get()
        self.emitter.streaming = True
        self.emitter.start_streaming_thread()

    def stop_stream(self):
        self.streaming = False
        self.emitter.streaming = False
        self.stream_frame.pack_forget()
        self.menu_frame.pack(expand=True)

    def change_filter(self, value):
        self.emitter.current_filter = value

    def update_frame(self, frame):
        if not self.streaming:
            return
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        frame = cv2.resize(frame, (800, 500))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.root.update_idletasks()