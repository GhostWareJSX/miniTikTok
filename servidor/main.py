import socket
import threading
import pickle
import struct

class VideoServer:
    def __init__(self, host='0.0.0.0', port=5002):
        # Inicializa el servidor en el host y puerto especificados
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        
    def start(self):
        # Inicia el servidor y acepta conexiones entrantes de clientes
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión establecida desde {addr}")
            self.clients.append(client_socket)
            # Crea un hilo para manejar cada cliente conectado
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        # Recibe frames de un cliente y los reenvía a los demás clientes conectados
        try:
            while True:
                # Recibir tamaño del frame (4 bytes)
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
                
                # Reenviar a todos los clientes menos al emisor
                self.broadcast(frame_data, client_socket)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Elimina el cliente de la lista y cierra el socket
            self.clients.remove(client_socket)
            client_socket.close()
    
    def broadcast(self, data, sender_socket):
        # Envía el frame recibido a todos los clientes excepto al emisor
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(struct.pack('!I', len(data)) + data)
                except:
                    self.clients.remove(client)
                    client.close()

if __name__ == "__main__":
    # Punto de entrada principal del servidor
    server = VideoServer()
    server.start()