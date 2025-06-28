import tkinter as tk
from PIL import Image, ImageTk
import struct
import socket
import cv2
import numpy as np
import pickle

class ReceiverUI:
    def __init__(self, receiver):
        self.receiver = receiver
        self.root = tk.Tk()
        self.root.title("Receptor de Video - TikTok-like")
        self.root.geometry("900x700")
        self.waiting = True

        # Frame del menú principal
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(expand=True)

        self.title_label = tk.Label(self.menu_frame, text="TikTokLive", font=("Arial", 32, "bold"))
        self.title_label.pack(pady=20)  # Antes: pady=40

        self.start_button = tk.Button(self.menu_frame, text="Recibir transmisión", font=("Arial", 18), command=self.start_receiving)
        self.start_button.pack(pady=20)

        self.quit_button = tk.Button(self.menu_frame, text="Salir", font=("Arial", 14), command=self.root.quit)
        self.quit_button.pack(pady=20)

        # Frame para la recepción de video
        self.stream_frame = tk.Frame(self.root)
        self.video_label = tk.Label(self.stream_frame, width=800, height=500, bg="black")
        self.video_label.pack(pady=20)

        self.waiting_label = tk.Label(self.stream_frame, text="En espera de la transmisión...", font=("Arial", 18), fg="gray")
        self.waiting_label.pack(pady=10)

        self.back_button = tk.Button(self.stream_frame, text="Volver al menú", font=("Arial", 14), command=self.back_to_menu)
        self.back_button.pack(pady=20)

    def run(self):
        self.root.mainloop()

    def start_receiving(self):
        self.menu_frame.pack_forget()
        self.stream_frame.pack(expand=True)
        self.waiting = True
        self.waiting_label.config(text="En espera de la transmisión...")
        import threading
        t = threading.Thread(target=self.receiver.start_receiving)
        t.daemon = True
        t.start()

    def back_to_menu(self):
        self.stream_frame.pack_forget()
        self.menu_frame.pack(expand=True)

    def update_frame(self, frame):
        if self.waiting:
            self.waiting = False
            self.waiting_label.config(text="")
        import cv2
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (800, 500))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.root.update_idletasks()

    def show_transmission_ended(self):
        self.waiting_label.config(text="La transmisión ha terminado.", fg="red")
        self.root.after(2000, self.back_to_menu)  # Espera 2 segundos y regresa al menú

    def receive_loop(self):
        first_frame = True
        while True:
            try:
                data = self.socket.recv(4)
                if not data or len(data) < 4:
                    if first_frame:
                        continue  # Sigue esperando el primer frame
                    else:
                        self.ui.show_transmission_ended()  # Muestra mensaje y regresa al menú
                        break
                size = struct.unpack('!I', data)[0]
                frame_data = b''
                while len(frame_data) < size:
                    try:
                        packet = self.socket.recv(size - len(frame_data))
                    except socket.timeout:
                        if first_frame:
                            continue
                        else:
                            break
                    if not packet:
                        break
                    frame_data += packet
                if len(frame_data) != size:
                    continue
                try:
                    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                except Exception:
                    frame = pickle.loads(frame_data)
                if frame is not None:
                    self.ui.update_frame(frame)
                    first_frame = False
            except socket.timeout:
                continue  # Espera sin bloquear
