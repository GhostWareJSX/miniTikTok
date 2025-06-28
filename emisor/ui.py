import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class EmitterUI:
    def __init__(self, emitter):
        self.emitter = emitter
        self.root = tk.Tk()
        self.root.title("Emisor de Video - TikTok-like")
        
        # Frame para el video
        self.video_frame = tk.Label(self.root)
        self.video_frame.pack()
        
        # Selector de filtros
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(
            self.root,
            textvariable=self.filter_var,
            values=[
                "Ninguno",
                "Escala de grises",
                "Negativo",
                "Espejo vertical",
                "Espejo horizontal",
                "Desenfoque",
                "Nitidez",
                "Bordes",
                "Detección de rostros",
                "Bigote",
                "Barba",
                "Lentes",
                "Sombrero",
                "Maquillaje"
            ]
        )
        self.filter_combobox.pack()
        self.filter_combobox.current(0)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # Botón de inicio
        self.start_button = tk.Button(self.root, text="Iniciar Transmisión", command=self.start_streaming)
        self.start_button.pack()
        
    def on_filter_change(self, event):
        selected_filter = self.filter_var.get()
        if selected_filter == "Ninguno":
            self.emitter.current_filter = None
        else:
            self.emitter.current_filter = selected_filter
    
    def start_streaming(self):
        self.start_button.config(state=tk.DISABLED)
        self.emitter.start_streaming()
    
    def update_frame(self, frame):
        # Convertir frame de OpenCV a formato para Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk)
        
        self.root.update()
    
    def run(self):
        self.root.mainloop()