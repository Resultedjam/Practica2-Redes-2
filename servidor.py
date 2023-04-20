import socket
import sys
import select
import selectors

HOST = 'localhost' #Se asigna la ip del servidor
PORT = 5000 #Puerto del servidor
buffer_size = 48522 #Tamaño maximo de datos a recibir

#Se utilizara el protocolo TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

sockets_list = [server_socket] #Lista creada para leer todos los sockets que
clients = {} #Vacio para recibir los datos del cliente
selector = selectors.DefaultSelector()
print("El servidor ha sido iniciado...")
print("Esperando conexion")
#empieza el proceso de conectar los sockets
while True:
    #Una vez la conexion es exitosa empieza la creacion del socket a usar
    read_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        #Si se cumple la "notified_socket" un nuevo cliente se ha conectado al servidor
        if notified_socket == server_socket:
            #Se acepta el cliente
            client_socket, client_address = server_socket.accept()
            selector.register(client_socket, selectors.EVENT_READ, read_sockets)#Se registra el nuevo socket con su correpondiente evento
            #Se asignan los datos del cliente que solicita el servidor
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            data = client_socket.recv(buffer_size)
            #Se notifica con que IP y puerto del cliente se hizo conexion
            print(f"Conexión establecida desde {client_address[0]}:{client_address[1]}")

        else:
            #En espera recibir los datos a traves de un socket
            data = client_socket.recv(buffer_size)
            if data:
                # Obtener el puerto del cliente
                client_port = client_socket.getpeername()[1]
                # Generar el nombre de archivo con el identificador del puerto
                file_name = f'audio_{client_port}.wav'
                # Aqui se recibe el audio y es transformado en .wav para poder ser escuchado sin corromperse
                with open(file_name, "wb") as f:
                    #En caso de no tener datos se termina el programa el ciclo while
                    while True:
                        data = client_socket.recv(buffer_size)
                        if not data:
                            break
                        f.write(data)

            else:
                #Una vez terminada la transferencia de archivos cierra la conexion con el cliente
                #o en caso de no haber recibido nada continua cerrando conexion
                sockets_list.remove(notified_socket)
                client_address = clients[notified_socket]
                del clients[notified_socket]

                print(f"Conexión cerrada desde {client_address[0]}:{client_address[1]}")
                selector.unregister(client_socket) #Elimina la lista de entrada de clientes
                notified_socket.close() #Se notifica que finalizo la conexcion con el cliente