import socket
import sys

port = sys.argv[1]  # Arreglo
port2 = int(port)  # Cast a int
ip = sys.argv[2]  # IP del servidor

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(('localhost', port2))
cliente_socket.sendall(b"Hola desde el cliente!!")
respuesta = cliente_socket.recv(1024)

print ("Respuesta del servidor: ", respuesta.decode())

cliente_socket.close()

