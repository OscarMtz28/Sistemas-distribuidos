import socket
import threading
import sys
import time
import os # Biblioteca que permite la lectura de archivos de la pc

# Función para manejar conexiones entrantes
def handle_peer(conn, addr):
    try:
        print(f"[+] Conectado desde {addr}")
        # Modificacion para leer informacion del archivo
        #data = conn.recv(1024).decode()
        #print(f"[{addr}] → {data}")
        #conn.sendall(f"Echo desde {conn.getsockname()}".encode())
        file = conn.recv(1024).decode()
        name, size = file.split("|")
        size = int(size)

        with open(name, "wb") as pr:  # Hacemos el cast del archivo para que se escriba en binario como bytes
            recived = 0 # Contador para los bytes recibidos
            while recived < size:
                data = conn.recv(4096) #Buffer
                if not data: # El archivo esta vacio? Se cierra
                    break
                pr.write(data) # La variable pr que contiene a nuestro archivo abierto escribe los bytes recibidos
                recived += len(data) # Actualiza el contador , la funcion "len" nos dice cuantos bytes acabamos de recibir
        print("Archivo recibido correctamente...")
        conn.sendall(f"Archivo {name} recibido".encode())
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
def connect_to_peers(peers, archivo):

    name = os.path.basename(archivo)
    size = os.path.getsize(archivo)

    for host, port in peers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                #archivo = "prueba.txt"
                info = f"{name}|{size}"
                sock.sendall(info.encode())
                with open(archivo, "rb") as pr: 
                    send = 0
                    while send < size:
                        data = pr.read (4096)
                        sock.sendall(data)
                        send += len(data)
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
        archivo = input("Ingrese la direccion del archivo .txt a enviat ( o 'exit' para salir): ")
        if archivo.lower() == 'exit':
            break
        connect_to_peers(peers, archivo)
