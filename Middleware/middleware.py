import socket
from threading import Thread
import itertools

# Lista de servidores destino (pueden estar en diferentes máquinas)
SERVERS = [
    ('localhost', 13000),
    ('localhost', 13001),
    ('localhost', 13002),
]

# Generador round-robin
server_cycle = itertools.cycle(SERVERS)

def handle_client(client_socket):
    target_host, target_port = next(server_cycle)
    try:
        # Conectarse al servidor de backend
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((target_host, target_port))

        # Reenviar la solicitud
        data = client_socket.recv(1024)
        server_socket.sendall(data)

        # Recibir respuesta y reenviarla al cliente
        response = server_socket.recv(1024)
        client_socket.sendall(response)
    except Exception as e:
        print("Error en el middleware:", e)
        client_socket.sendall(b"Error en el middleware")
    finally:
        client_socket.close()
        server_socket.close()

def start_middleware(host='localhost', port=12345):
    middleware_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    middleware_socket.bind((host, port))
    middleware_socket.listen(5)
    print(f"Middleware escuchando en {host}:{port}")

    try:
        while True:
            client_sock, addr = middleware_socket.accept()
            print(f"Conexión entrante de {addr}")
            thread = Thread(target=handle_client, args=(client_sock,))
            thread.start()
    except KeyboardInterrupt:
        print("Middleware detenido manualmente.")
    finally:
        middleware_socket.close()

if __name__ == "__main__":
    start_middleware()
