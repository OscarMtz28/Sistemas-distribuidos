import socket
import threading
import sys
import time

# Función para manejar conexiones entrantes
def handle_peer(conn, addr):
    try:
        print(f"[+] Conectado desde {addr}")
        data = conn.recv(1024).decode()
        print(f"[{addr}] → {data}")
        conn.sendall(f"Echo desde {conn.getsockname()}".encode())
    except Exception as e:
        print(f"[!] Error con {addr}: {e}")
    finally:
        conn.close()

# Servidor que escucha conexiones entrantes
def peer_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[SERVIDOR] Nodo escuchando en puerto {port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_peer, args=(conn, addr))
        thread.start()

# Cliente que envía mensajes a otros peers
def connect_to_peers(peers, message):
    for host, port in peers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                sock.sendall(message.encode())
                response = sock.recv(1024).decode()
                print(f"[{host}:{port}] ⇐ {response}")
        except Exception as e:
            print(f"[!] No se pudo conectar a {host}:{port} - {e}")

# Programa principal
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python peer_node.py <mi_puerto> <peer1_host:port> [<peer2_host:port> ...]")
        sys.exit(1)

    my_port = int(sys.argv[1])
    peers = [tuple(p.split(":")) for p in sys.argv[2:]]
    peers = [(h, int(p)) for h, p in peers if int(p) != my_port]

    # Iniciar el hilo del servidor
    threading.Thread(target=peer_server, args=(my_port,), daemon=True).start()

    # Dar tiempo a que el servidor escuche
    time.sleep(1)

    # Enviar mensaje a los peers conocidos
    while True:
        mensaje = input("Mensaje a enviar (o 'exit'): ")
        if mensaje.lower() == 'exit':
            break
        connect_to_peers(peers, mensaje)
