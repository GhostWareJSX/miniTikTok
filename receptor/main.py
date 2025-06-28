import cv2
import socket
import struct
import pickle
import numpy as np
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
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def start_receiving(self):
        try:
            while True:
                # Recibir tamaño del frame
                data = self.socket.recv(4)
                if not data:
                    break
                
                size = struct.unpack('!I', data)[0]
                # Recibir frame serializado
                frame_data = b''
                while len(frame_data) < size:
                    packet = self.socket.recv(size - len(frame_data))
                    if not packet:
                        break
                    frame_data += packet
                
                if len(frame_data) != size:
                    continue
                
                # Deserializar frame
                try:
                    # Si el servidor envía imágenes comprimidas (por ejemplo, JPEG)
                    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                except Exception:
                    # Si el servidor usa pickle
                    frame = pickle.loads(frame_data)
                self.ui.update_frame(frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"Error al recibir frame: {e}")
        finally:
            self.socket.close()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    receiver = VideoReceiver()
    if receiver.connect():
        receiver.start_receiving()