import socket
import struct
import pickle
import numpy as np
import cv2
from ui import ReceiverUI

class VideoReceiver:
    def __init__(self, server_host='localhost', server_port=5002):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ui = ReceiverUI(self)

    def connect(self):
        try:
            self.socket.connect((self.server_host, self.server_port))
            self.socket.settimeout(1.0)  # Timeout de 1 segundo
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    def start_receiving(self):
        if not self.connect():
            print("No se pudo conectar al servidor.")
            return
        try:
            first_frame = True
            while True:
                try:
                    data = self.socket.recv(4)
                    if not data or len(data) < 4:
                        if first_frame:
                            continue  # Sigue esperando el primer frame
                        else:
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
        except Exception as e:
            print(f"Error al recibir frame: {e}")
        finally:
            self.socket.close()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    receiver = VideoReceiver()
    receiver.ui.run()