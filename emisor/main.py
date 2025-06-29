import cv2
import socket
import struct
import pickle
import numpy as np
import threading
from filters import apply_filter
from ui import EmitterUI

class VideoEmitter:
    def __init__(self, server_host='192.168.1.255', server_port=5002):  # Cambia aquí la IP
        # Inicializa el emisor de video con la dirección del servidor
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None  # El socket se crea al conectar
        self.cap = None
        self.current_filter = None
        self.streaming = False
        self.ui = EmitterUI(self)

    def connect(self):
        # Crea y conecta un nuevo socket al servidor
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    def start_streaming_thread(self):
        # Inicia la transmisión en un hilo separado
        t = threading.Thread(target=self.start_streaming)
        t.daemon = True
        t.start()

    def start_streaming(self):
        # Captura video de la cámara, aplica filtro y envía los frames al servidor
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
        if not self.connect():
            print("No se pudo conectar al servidor.")
            self.streaming = False
            return
        while self.streaming and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.current_filter:
                frame = apply_filter(frame, self.current_filter)
            self.ui.update_frame(frame)
            self.send_frame(frame)
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.socket:
            self.socket.close()
            self.socket = None  # Libera el socket

    def send_frame(self, frame):
        # Codifica y envía un frame al servidor
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error al codificar el frame")
                return
            data = buffer.tobytes()
            if self.socket:
                self.socket.sendall(struct.pack('!I', len(data)) + data)
        except Exception as e:
            print(f"Error al enviar frame: {e}")

if __name__ == "__main__":
    # Punto de entrada principal del emisor
    emitter = VideoEmitter()
    emitter.ui.start()