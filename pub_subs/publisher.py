import socket
def main():
    broker_host = 'localhost'
    broker_port = 14000
    print("Publicador listo. Usa formato <topic:mensaje>")
    while True:
        try:
            user_input = input(">> ")
            if user_input.lower() in ['exit','quit']:
                break
            topic,message = user_input.split(":", 1)
            msg = f"PUB:{topic}:{message}"
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((broker_host, broker_port))
                sock.sendall(msg.encode())
        except Exception as e:
            print(f"[!] Error: {e}")
if __name__ == "__main__":
    main()