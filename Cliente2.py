import socket
import sys
import time
HOST = 'localhost'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Envia la solicitud de conexion al server
try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("No se pudo conectar al servidor")
    sys.exit()
#Selecciona el archivo a enviar en formato binario
with open("orchid.mp3", "rb") as f:
    audio_data = f.read()

client_socket.sendall(audio_data)
client_socket.shutdown(socket.SHUT_RDWR)
client_socket.close()