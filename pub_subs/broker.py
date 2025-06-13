import socket
import threading
subscribers = {} #Topic ---> Lista de los sockets de los subscritos
lock = threading.Lock()
def handle_client(conn, addr):
    try:
        msg_type = conn.recv(1024).decode().strip()
        if msg_type.startswith("PUB:"):
            parts = msg_type[4:].split(":", 1)
            if len(parts) != 2:
                conn.close()
                return
            topic, message = parts
            print (f"[>] Pubilcacion en '{topic}':'{message}'")
            with lock:
                for sub in subscribers.get(topic, []):
                    try:
                        sub.sendall(f"[{topic}] {message}".encode())
                    except:
                        continue
        else:
            conn.sendall(b"Comando no reconocido")
    except Exception as e:
        print(f"[!] Error con {addr}: {e}")
    finally:
        conn.close()
def start_broker(host='localhost', port = 14000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[BROKER] Escuchando en {host}:{port} ...")
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn,addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Broker detenido")
    finally:
        server.close()
if __name__ == "__main__":
    start_broker()
