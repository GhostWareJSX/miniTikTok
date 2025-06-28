import socket
import threading
import pickle
import struct

class VideoServer:
    def __init__(self, host='0.0.0.0', port=5002):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión establecida desde {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        try:
            while True:
                # Recibir tamaño del frame
                data = client_socket.recv(4)
                if not data:
                    break
                
                size = struct.unpack('!I', data)[0]
                # Recibir frame serializado
                frame_data = b''
                while len(frame_data) < size:
                    packet = client_socket.recv(size - len(frame_data))
                    if not packet:
                        break
                    frame_data += packet
                
                if len(frame_data) != size:
                    continue
                
                # Reenviar a todos los clientes
                self.broadcast(frame_data, client_socket)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()
    
    def broadcast(self, data, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(struct.pack('!I', len(data)) + data)
                except:
                    self.clients.remove(client)
                    client.close()

if __name__ == "__main__":
    server = VideoServer()
    server.start()