import cv2
import socket
import struct
import pickle
import numpy as np
from filters import apply_filter
from ui import EmitterUI

class VideoEmitter:
    def __init__(self, server_host='localhost', server_port=5002):
        print("Inicializando VideoEmitter...")
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket creado")
        self.cap = cv2.VideoCapture(0)
        print("Cámara inicializada")
        self.current_filter = None
        try:
            self.ui = EmitterUI(self)
            print("UI inicializada")
        except Exception as e:
            print(f"Error al inicializar la UI: {e}")
        
    def connect(self):
        try:
            self.socket.connect((self.server_host, self.server_port))
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def start_streaming(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Aplicar filtro seleccionado
            if self.current_filter:
                frame = apply_filter(frame, self.current_filter)
            
            # Mostrar frame localmente
            self.ui.update_frame(frame)
            
            # Enviar frame al servidor
            self.send_frame(frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        self.socket.close()
        cv2.destroyAllWindows()
    
    def send_frame(self, frame):
        try:
            # Codificar el frame como JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error al codificar el frame")
                return
            data = buffer.tobytes()
            # Enviar tamaño del frame y luego el frame
            self.socket.sendall(struct.pack('!I', len(data)) + data)
        except Exception as e:
            print(f"Error al enviar frame: {e}")

if __name__ == "__main__":
    print("Iniciando emisor...")
    emitter = VideoEmitter()
    if emitter.connect():
        print("Conectado al servidor, iniciando streaming...")
        emitter.start_streaming()
    else:
        print("No se pudo conectar al servidor.")