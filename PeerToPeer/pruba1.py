import socket
import threading
import sys
import os
import time

# Función para manejar conexiones entrantes (recibe archivos)
def handle_peer(conn, addr):
    try:
        print(f"\n[+] Conexión entrante desde {addr}")
        
        # Recibir información del archivo
        file_info = conn.recv(1024).decode()
        if not file_info:
            return
            
        filename, filesize = file_info.split("|")
        filesize = int(filesize)
        
        print(f"Recibiendo archivo: {filename} ({filesize} bytes)")
        
        # Recibir el archivo en bloques
        with open(filename, "wb") as f:
            bytes_received = 0
            while bytes_received < filesize:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)
                
        print(f"Archivo recibido correctamente")
        conn.sendall(f"Archivo {filename} recibido".encode())
        
    except Exception as e:
        print(f"[!] Error con {addr}: {e}")
    finally:
        conn.close()

# Servidor que escucha conexiones entrantes (igual al original)
def peer_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[SERVIDOR] Escuchando en puerto {port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_peer, args=(conn, addr))
        thread.start()

# Función para enviar archivos (similar a connect_to_peers original)
def send_file_to_peers(peers, filepath):
    if not os.path.exists(filepath):
        print(f"[!] Archivo {filepath} no encontrado")
        return
        
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    for host, port in peers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                
                print(f"\nEnviando {filename} a {host}:{port}")
                
                # Enviar metadatos del archivo
                file_info = f"{filename}|{filesize}"
                sock.sendall(file_info.encode())
                
                # Enviar el archivo en bloques
                with open(filepath, "rb") as f:
                    bytes_sent = 0
                    while bytes_sent < filesize:
                        data = f.read(4096)
                        sock.sendall(data)
                        bytes_sent += len(data)
                
                # Recibir confirmación
                response = sock.recv(1024).decode()
                print(f"Respuesta: {response}")
                
        except Exception as e:
            print(f"[!] Error con {host}:{port} - {e}")

# Programa principal (similar al original)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python peer_node.py <mi_puerto> <peer1_host:port> [<peer2_host:port> ...]")
        sys.exit(1)

    my_port = int(sys.argv[1])
    peers = [tuple(p.split(":")) for p in sys.argv[2:]]
    peers = [(h, int(p)) for h, p in peers if int(p) != my_port]

    # Iniciar el hilo del servidor (igual al original)
    server_thread = threading.Thread(target=peer_server, args=(my_port,))
    server_thread.daemon = True
    server_thread.start()

    # Pequeña pausa para que el servidor inicie
    time.sleep(1)

    # Bucle principal similar al original pero para archivos
    while True:
        filepath = input("\nIngrese la ruta del archivo .txt a enviar (o 'exit' para salir): ")
        
        if filepath.lower() == 'exit':
            break
            
        if not filepath.endswith('.txt'):
            print("Error: Solo se permiten archivos .txt")
            continue
            
        send_file_to_peers(peers, filepath)

    print("\nCerrando programa...")
    sys.exit(0)