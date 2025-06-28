import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class ReceiverUI:
    def __init__(self, receiver):
        self.receiver = receiver
        self.root = tk.Tk()
        self.root.title("Receptor de Video - TikTok-like")
        
        # Frame para el video
        self.video_frame = tk.Label(self.root)
        self.video_frame.pack()
        
        # Botón de inicio
        self.start_button = tk.Button(self.root, text="Iniciar Recepción", command=self.start_receiving)
        self.start_button.pack()
        
    def start_receiving(self):
        self.start_button.config(state=tk.DISABLED)
        self.receiver.start_receiving()
    
    def update_frame(self, frame):
        # Convertir frame de OpenCV a formato para Tkinter
        if len(frame.shape) == 2:  # Si es escala de grises
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk)
        
        self.root.update()
    
    def run(self):
        self.root.mainloop()