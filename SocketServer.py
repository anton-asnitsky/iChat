import socket
import select


class SocketServer:
    def __init__(self):
        self.HEADER_LENGTH = 10

        self.IP = "127.0.0.1"
        self.PORT = 1234

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen()

        self.sockets_list = [self.server_socket]

        self.clients = {}

        print(f'Listening for connections on {self.IP}:{self.PORT}...')

    def start(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

            for notified_socket in read_sockets:

                if notified_socket == self.server_socket:

                    client_socket, client_address = self.server_socket.accept()
                    user = self.receive_message(client_socket)

                    if user is False:
                        continue

                    self.sockets_list.append(client_socket)
                    self.clients[client_socket] = user

                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]}, "
                          f"username: {user['data'].decode('utf-8')}")

                else:
                    message = self.receive_message(notified_socket)

                    if message is False:
                        print(f"Closed connection from: {self.clients[notified_socket]['data'].decode('utf-8')}")

                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]

                        continue

                    user = self.clients[notified_socket]
                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

                    for client_socket in self.clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    def receive_message(self, incoming_socket):
        try:
            message_header = incoming_socket.recv(self.HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())

            return {'header': message_header, 'data': incoming_socket.recv(message_length)}

        except Exception as e:
            print(f"Unable to process message, reason: {str(e)}")
            return False


server = SocketServer()
server.start()
